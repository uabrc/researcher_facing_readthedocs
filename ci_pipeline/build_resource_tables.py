import argparse
import re
import shutil
from pathlib import Path, PurePath
from typing import List, Union

import pandas as pd

PathLike = Union[Path, PurePath, str]


RES_FOLDER = PurePath("res")
PARTITION_FILE = RES_FOLDER / "partition.csv"
HARDWARE_FILE = RES_FOLDER / "hardware.csv"

COMPUTE_TYPE = "Compute Type"
CORES_PER_DIE = "Cores Per Die"
CORES_PER_NODE = "Cores Per Node"
CPU_INFO = "CPU Info"
CPU_TFLOPS_PER_NODE = "CPU TFLOPS Per Node"
DIES_PER_NODE = "Dies Per Node"
DIE_FREQUENCY_GHZ = "Die Frequency GHz"
DIE_INSTRUCTIONS_PER_CYCLE_FLOAT64 = "Die Instructions Per Cycle Float64"
DIE_MAKE = "Die Make"
DIE_MODEL = "Die Model"
FABRIC = "Fabric"
GB = "GB"
GENERATION = "Generation"
GHZ = "GHz"
GPU_CUDA_CORES = "GPU CUDA Cores"
GPU_FREQUENCY_GHZ = "GPU Frequency GHz"
GPU_INFO = "GPU Info"
GPU_INSTRUCTIONS_PER_CYCLE_FLOAT64 = "GPU Instructions Per Cycle Float64"
GPU_MAKE = "GPU Make"
GPU_MEMORY_GB = "GPU Memory GB"
GPU_MODEL = "GPU Model"
GPU_PER_NODE = "GPU Per Node"
GPU_TFLOPS_PER_NODE = "GPU TFLOPS Per Node"
GPU_TFLOPS_PER_NODE = "GPU TFLOPS Per Node"
HPC = "hpc"
IN_USE = "In Use"
MEMORY_PER_NODE_GB = "Memory Per Node GB"
NODES = "Nodes"
PARTITION = "Partition"
TFLOPS = "TFLOPS"
TFLOPS_PER_CORE = "TFLOPS Per Core"
TFLOPS_PER_GPU = "TFLOPS Per GPU"
TFLOPS_PER_NODE = "TFLOPS Per Node"
TOTAL = "Total"
TOTAL_CORES = "Total Cores"
TOTAL_GPUS = "Total GPUs"
TOTAL_MEMORY_GB = "Total Memory GB"


def build_partition_table() -> pd.DataFrame:
    df = _read_partition_table()
    df = df.rename(columns=_to_pretty_column)
    return df


def build_flops_table(fabric: str) -> pd.DataFrame:
    df = _read_hardware_table(fabric=fabric)

    df[TFLOPS_PER_CORE] = (
        df[DIE_FREQUENCY_GHZ] * df[DIE_INSTRUCTIONS_PER_CYCLE_FLOAT64] / 1000
    )
    df[CPU_TFLOPS_PER_NODE] = df[TFLOPS_PER_CORE] * df[CORES_PER_NODE]
    df[TFLOPS_PER_GPU] = (
        df[GPU_FREQUENCY_GHZ]
        * df[GPU_INSTRUCTIONS_PER_CYCLE_FLOAT64]
        * df[GPU_CUDA_CORES]
        / 1000
    )
    df[GPU_TFLOPS_PER_NODE] = df[TFLOPS_PER_GPU] * df[GPU_PER_NODE]
    df[GPU_TFLOPS_PER_NODE + "_DUMMY"] = df[GPU_TFLOPS_PER_NODE].fillna(
        0.0
    )  # use a dummy col to avoid printing 0.0
    df[TFLOPS_PER_NODE] = df[CPU_TFLOPS_PER_NODE] + df[GPU_TFLOPS_PER_NODE + "_DUMMY"]
    df[TFLOPS] = df[TFLOPS_PER_NODE] * df[NODES]

    COLS = [
        GENERATION,
        CPU_TFLOPS_PER_NODE,
        GPU_TFLOPS_PER_NODE,
        TFLOPS_PER_NODE,
        NODES,
        TFLOPS,
    ]
    df = df[COLS]

    COLS = [TFLOPS]
    df = _append_total_row(df=df, cols=COLS)

    COLS = [
        CPU_TFLOPS_PER_NODE,
        GPU_TFLOPS_PER_NODE,
        TFLOPS_PER_NODE,
        TFLOPS,
    ]
    df[COLS] = df[COLS].applymap(lambda x: _clean_float_to_str(x=x, fmt="{:,.2f}"))

    df = df.rename(columns=_to_pretty_column)
    df = df.astype("string")
    df = df.fillna("")

    df.loc[TOTAL, GENERATION] = "TOTAL"  # type: ignore

    return df


def _clean_float_to_str(x, fmt: str) -> str:
    if pd.isna(x):
        x = ""
    else:
        x = fmt.format(x)
    return x


def build_full_hardware_table(fabric: str) -> pd.DataFrame:
    df = _read_hardware_table(fabric=fabric)

    COLS = [
        GENERATION,
        COMPUTE_TYPE,
        PARTITION,
        TOTAL_CORES,
        TOTAL_MEMORY_GB,
        TOTAL_GPUS,
        CORES_PER_NODE,
        CORES_PER_DIE,
        DIES_PER_NODE,
        DIE_MAKE,
        DIE_MODEL,
        DIE_FREQUENCY_GHZ,
        MEMORY_PER_NODE_GB,
        GPU_PER_NODE,
        GPU_MAKE,
        GPU_MODEL,
        GPU_MEMORY_GB,
        NODES,
    ]
    df = df[COLS].copy()
    df = df.rename(columns=_to_pretty_column)

    df = df.astype("string")
    df = df.fillna("")

    return df


def build_short_hardware_table(fabric: str) -> pd.DataFrame:
    df = _read_hardware_table(fabric=fabric)

    COLS = [
        GENERATION,
        COMPUTE_TYPE,
        PARTITION,
        TOTAL_CORES,
        TOTAL_MEMORY_GB,
        TOTAL_GPUS,
        CORES_PER_NODE,
        MEMORY_PER_NODE_GB,
        NODES,
        CPU_INFO,
        GPU_INFO,
    ]
    df = df[COLS].copy()
    COLS = [
        TOTAL_CORES,
        TOTAL_MEMORY_GB,
        TOTAL_GPUS,
        NODES,
    ]
    df = _append_total_row(df=df, cols=COLS)
    df = df.rename(columns=_to_pretty_column)

    df = df.astype("string")
    df = df.fillna("")

    df.loc[TOTAL, GENERATION] = "TOTAL"  # type: ignore

    return df


def build_sample_grant_blurb(
    df_short_hardware: pd.DataFrame, df_flops: pd.DataFrame
) -> str:
    hw = df_short_hardware
    tf = df_flops
    tflops = float(str(tf.loc[TOTAL, TFLOPS]))
    s = [
        "UAB IT Research Computing maintains high performance compute (HPC) and storage resources for investigators.",
        "The Cheaha high performance compute cluster provides",
        f"{hw.loc[TOTAL, TOTAL_CORES]} CPU cores and {hw.loc[TOTAL, TOTAL_GPUS]} GPUs",
        "interconnected via an InfiniBand network, providing over",
        f"{tflops:.0f} TFLOP/s of aggregate theoretical peak performance.",
        "A high-performance, 12PB raw GPFS storage on DDN SFA12KX hardware is also connected to these compute nodes via the Infiniband fabric, available to all UAB investigators.",
    ]
    return " ".join(s)


def _read_partition_table() -> pd.DataFrame:
    df = pd.read_csv(PARTITION_FILE)
    return df


def _read_hardware_table(fabric: str) -> pd.DataFrame:
    df = pd.read_csv(HARDWARE_FILE)
    df = _preprocess_hardware_table(df=df, fabric=fabric)
    return df


def _preprocess_hardware_table(df: pd.DataFrame, fabric: str) -> pd.DataFrame:
    df = df[df[IN_USE] == 1]  # type: ignore
    df = df[df[FABRIC] == fabric]  # type: ignore

    COLS = [
        GENERATION,
        CORES_PER_DIE,
        DIES_PER_NODE,
        MEMORY_PER_NODE_GB,
        GPU_PER_NODE,
        GPU_MEMORY_GB,
        NODES,
    ]
    df[COLS] = df[COLS].astype("Int64")

    df[TOTAL_CORES] = df[CORES_PER_DIE] * df[DIES_PER_NODE] * df[NODES]
    df[TOTAL_MEMORY_GB] = df[MEMORY_PER_NODE_GB] * df[NODES]
    df[TOTAL_GPUS] = df[GPU_PER_NODE] * df[NODES]
    df[CORES_PER_NODE] = df[CORES_PER_DIE] * df[DIES_PER_NODE]

    df[CPU_INFO] = (
        df[DIE_MAKE]
        + " "
        + df[DIE_MODEL]
        + " "
        + df[DIE_FREQUENCY_GHZ].map("{:,.2f}".format)
        + " "
        + GHZ
    )
    df[GPU_INFO] = (
        df[GPU_MAKE]
        + " "
        + df[GPU_MODEL]
        + " "
        + df[GPU_MEMORY_GB].map("{0:.0f}".format)
        + " "
        + GB
    )

    return df


def _append_total_row(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    for col in cols:
        df.loc[TOTAL, col] = df[col].sum()  # type: ignore
    return df


def _dump(file_path: PathLike, s: str) -> None:
    with open(file=file_path, mode="w") as f:
        f.write(s)


# def _to_mediawiki(df: pd.DataFrame) -> str:
#     doc_l = []

#     doc_l.append('{| class="wikitable"\n')

#     header_l = list(df.columns)
#     header_f = "!" + "!!\t".join(header_l) + "\n"
#     doc_l.append(header_f)

#     for row in df.itertuples(index=False):
#         row = list(row)
#         row = [str(x) for x in row]
#         row_f = "|" + '||align="right"|\t'.join(row) + "\n"
#         doc_l.append(row_f)

#     doc_l.append("|}\n")
#     doc_f = "|-\n".join(doc_l)

#     return doc_f


def _to_pretty_column(col: str) -> str:
    col = re.sub(
        pattern="[_](.{0,1})",
        repl=lambda match: " " + match.group(1).upper(),
        string=col,
    )
    col = re.sub(
        pattern="^(.{0,1})", repl=lambda match: match.group(1).upper(), string=col,
    )
    return col


def interface():
    parser = argparse.ArgumentParser(
        description="Builds hardware tables for Cheaha readthedocs."
    )
    parser.add_argument(
        "output_folder",
        metavar="output folder",
        type=PurePath,
        nargs=1,
        help="Output folder for tables.",
    )
    parser.add_argument(
        "-f",
        "--fabric",
        type=str,
        nargs=1,
        required=False,
        default=HPC,
        help="Fabric to produce tables for.",
    )
    args = parser.parse_args()
    output_folder: PurePath = args.output_folder[0]
    selected_fabric: str = args.fabric[0]

    df_full_hardware = build_full_hardware_table(fabric=selected_fabric)
    df_full_hardware.to_csv(output_folder / "hardware_full_df.csv", index=False)
    # mw = _to_mediawiki(df=df_flops)
    # _dump(file_path=output_folder / "hardware_full_mw.txt", s=mw)

    df_short_hardware = build_short_hardware_table(fabric=selected_fabric)
    df_short_hardware.to_csv(output_folder / "hardware_short_df.csv", index=False)
    # mw = _to_mediawiki(df=df_flops)
    # _dump(file_path=output_folder / "hardware_short_mw.txt", s=mw)

    df_flops = build_flops_table(fabric=selected_fabric)
    df_flops.to_csv(output_folder / "tflops_df.csv", index=False)
    # df.loc["total", "Generation"] = "TOTAL"  # type: ignore
    # mw = _to_mediawiki(df=df_flops)
    # _dump(file_path=output_folder / "tflops_mw.txt", s=mw)

    # df_partition = build_partition_table()
    # mw = _to_mediawiki(df=df_partition)
    # _dump(file_path=output_folder / "partition_mw.txt", s=mw)

    shutil.copyfile(PARTITION_FILE, output_folder / PARTITION_FILE.name)

    blurb = build_sample_grant_blurb(
        df_short_hardware=df_short_hardware, df_flops=df_flops
    )
    _dump(file_path=output_folder / "grant_blurb_short.txt", s=blurb)


if __name__ == "__main__":
    interface()
