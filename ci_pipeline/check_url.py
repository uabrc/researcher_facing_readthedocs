import re
from pathlib import Path, PurePath
from typing import List, Optional, Union

import requests

PathLike = Union[Path, PurePath, str]

SOURCE = PurePath(".") / "source"

# CUSTOM ACTIONS
def get_status(url: str, text: str) -> Optional[str]:
    try:
        response = requests.get(url=url)
        status = response.status_code
        if status == 200:
            out = None
        else:
            out = text.format(url=url, status=str(status))
    except Exception as e:
        out = str(e)
    return out


# CHECK DEFINITIONS
# 1. "action" must be None or a function from CUSTOM ACTIONS above. If it is
#    None then "text" must be a plain string. If it is a function, it must take
#    the match returned by "pattern" and it must take the format string "text". The function must
#    return None or a string. None signals that it passes the check and nothing
#    will be printed. A string will be printed.
# 2. "pattern" is a regex string returning 0 or 1 matches. Multiple matches are
#    not supported.
# 3. "text" must be a plain string or a format string.


CHECKS = [
    {
        "action": None,
        "pattern": re.compile(r"^(http://.*)$"),
        "text": "Only use https in URLs",
    },
    {
        "action": None,
        "pattern": re.compile(r"^(http[s]+://.*)$"),
        "text": "Format all external links like the following `Optional link text <https://www.url.com>`__",
    },
    {
        "action": None,
        "pattern": re.compile(r"`(?:[^<> ]*? )*?<(.*?)>`_"),
        "text": "Use double trailing underscore instead of single to make explicit target into anonymous target",
    },
    {
        "action": get_status,
        "pattern": re.compile(r"`(?:[^<> ]*? )*?<(.*?)>`__"),
        "text": "URL<{url}> STATUS[{status}]",
    },
]


# CODE
def interface() -> None:
    assert Path(SOURCE).is_dir()
    paths = Path(SOURCE).glob("**/*.rst")
    results = []
    for path in paths:
        lines = read_file(path)
        file_results = check_file(path=path, lines=lines, checks=CHECKS)
        results.extend(file_results)

    print_results(results)


def check_file(path: PathLike, lines: List[str], checks: List[dict]) -> List[str]:
    results = []
    for line_number, line in enumerate(lines):
        line_results = check_line(
            path=path, line_number=line_number, line=line, checks=checks
        )
        results.extend(line_results)
    return results


def check_line(
    path: PathLike, line_number: int, line: str, checks: List[dict]
) -> List[str]:
    results = []
    for check in checks:
        pattern = check["pattern"]
        matches: List[str] = re.findall(pattern=pattern, string=line)
        match_results = check_matches(
            path=path, line_number=line_number, check=check, matches=matches
        )
        results.extend(match_results)
    return results


def check_matches(
    path: PathLike, line_number: int, check: dict, matches: List[str]
) -> List[str]:
    out_text = None
    text_template = check["text"]
    action = check["action"]
    results = []
    for match in matches:
        if action is not None:
            out_text = action(match, text_template)
        else:
            out_text = text_template
        if out_text is not None:
            result = f"{str(path)}:{line_number} {out_text}"
            results.append(result)
    return results


def read_file(path: PathLike) -> List[str]:
    with open(path, "r") as f:
        lines = f.readlines()
    return lines


def print_results(results: List[str]) -> None:
    out = "\n".join(results)
    print(out)


if __name__ == "__main__":
    interface()
