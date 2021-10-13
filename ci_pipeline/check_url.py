import re
from pathlib import Path, PurePath
from typing import Any, Dict, List, Tuple, Union

import requests

PathLike = Union[Path, PurePath, str]

SOURCE = PurePath(".") / "source"

FAIL_REGEXES = {
    r"http://": "Only use https in URLs",
    r"http[s]+://": "Format all external links like `Optional link text <https://www.url.com>`_",
}
CHECK_RESPONSE_REGEX = re.compile(r"`(?:[^<> ]*? )*?<(.*?)>`_")


def interface() -> None:
    assert Path(SOURCE).is_dir()
    paths = Path(SOURCE).glob("**/*.rst")
    issues = {}
    for path in paths:
        issues[path] = check_file(path)

    for path, path_issues in issues.items():
        for issue in path_issues:
            print_issue(path=path, issue=issue)


def check_file(path: PathLike) -> List[Dict[str, Any]]:
    contents = load_contents(path=path)
    urls, linenos = find_urls(contents)
    issues = []
    for url, lineno in zip(urls, linenos):
        issue = {"lineno": lineno, "url": url}
        try:
            status = get_status(url=url)
            if status == 200:
                continue
            status = str(status)
        except requests.exceptions.MissingSchema as e:
            status = str(e)
        issue["status"] = status
        issues.append(issue)
    return issues


def print_issue(path: PathLike, issue: Dict[str, Any]) -> None:
    url = issue["url"]
    lineno = issue["lineno"]
    status = issue["status"]
    print(f"{path}:{lineno} URL<{url}> STATUS[{status}]")


def load_contents(path: PathLike) -> List[str]:
    with open(path, "r") as f:
        contents = f.readlines()
    return contents


def find_urls(contents: List[str]) -> Tuple[List[str], List[int]]:
    urls = []
    linenos = []
    for lineno, line in enumerate(contents):
        line_urls = re.findall(CHECK_RESPONSE_REGEX, line)
        for url in line_urls:
            urls.append(url)
            linenos.append(lineno)
    return (urls, linenos)


def get_status(url: str) -> int:
    response = requests.get(url=url)
    return response.status_code


if __name__ == "__main__":
    interface()
