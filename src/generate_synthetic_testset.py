"""
------------------------------------------------------------------------------
OFAX - Merge OFAC Search Result Files
Author : Suprakash Mukherjee

Description
-----------
Merges all downloaded OFAC Excel files into a single consolidated dataset.

Input
-----
./downloads_processed/*.xlsx

Output
------
./output/synthetic_data_OFAC_<YYYY-MM-DD>.xlsx

Usage
-----
python merge_ofac_xlsx.py
------------------------------------------------------------------------------
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

# =============================================================================
# Project Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DOWNLOADS_DIR = PROJECT_ROOT / "downloads_processed"
OUTPUT_DIR = PROJECT_ROOT / "output"

COLUMN_NAMES = [
    "Name",
    "Address",
    "Type",
    "Program(s)",
    "List",
    "Score",
]

EXPECTED_COLUMNS = ["FILENAME"] + COLUMN_NAMES


def merge_ofac_xlsx(
    downloads_dir: Path = DOWNLOADS_DIR,
    output_dir: Path = OUTPUT_DIR,
):
    """
    Merge all downloaded OFAC Excel files into a single Excel dataset.

    Parameters
    ----------
    downloads_dir : Path
        Directory containing downloaded OFAC Excel files.

    output_dir : Path
        Directory where the merged output will be saved.

    Returns
    -------
    tuple
        (
            output_file,
            successful_files,
            failed_files
        )
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    if not downloads_dir.exists():
        raise FileNotFoundError(
            f"Downloads directory not found:\n{downloads_dir}"
        )

    today = datetime.now().strftime("%Y-%m-%d")

    output_file = output_dir / f"synthetic_data_OFAC_{today}.xlsx"

    xlsx_files = sorted(downloads_dir.glob("*.xlsx"))

    if not xlsx_files:
        raise FileNotFoundError(
            f"No Excel files found in:\n{downloads_dir}"
        )

    frames = []
    successful_files = []
    failed_files = []

    for file in xlsx_files:

        try:

            df = pd.read_excel(file)

            df = df.iloc[:, : len(COLUMN_NAMES)]

            df.insert(0, "FILENAME", file.name)

            frames.append(df)

            successful_files.append(file.name)

            print(
                f"[+] Loaded : {file.name} | Rows = {len(df)}"
            )

        except Exception as e:

            failed_files.append((file.name, str(e)))

            print(
                f"[!] Failed : {file.name}\n"
                f"    Error : {e}"
            )

    if not frames:
        raise ValueError(
            "No valid Excel files could be processed."
        )

    combined = pd.concat(frames, ignore_index=True)

    combined.columns = EXPECTED_COLUMNS

    combined.to_excel(
        output_file,
        index=False,
        engine="openpyxl",
    )

    print("\n" + "=" * 60)
    print("OFAX Merge Summary")
    print("=" * 60)

    print(f"Input Files Found      : {len(xlsx_files)}")
    print(f"Successfully Processed : {len(successful_files)}")
    print(f"Failed Files           : {len(failed_files)}")
    print(f"Total Rows             : {len(combined):,}")
    print(f"Output File            : {output_file}")

    if failed_files:

        print("\nFailed Files")

        for filename, error in failed_files:

            print(f" - {filename}")

    print("=" * 60)

    return (
        output_file,
        successful_files,
        failed_files,
    )


if __name__ == "__main__":

    merge_ofac_xlsx()