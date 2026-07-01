"""
------------------------------------------------------------------------------
OFAX - OFAC XLS to XLSX Converter
Author : Suprakash Mukherjee

Description
-----------
Converts all downloaded OFAC ".xls" files (HTML-based Excel files)
into modern ".xlsx" format for downstream processing.

Input
-----
./downloads/*.xls

Output
------
./downloads_processed/*.xlsx

Project Structure
-----------------
OFAX/
│
├── downloads/
│
├── downloads_processed/
│
└── src/
    └── convert_xls_to_xlsx.py

Usage
-----
python convert_xls_to_xlsx.py
------------------------------------------------------------------------------
"""

from pathlib import Path

import pandas as pd

# =============================================================================
# Project Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

INPUT_DIR = PROJECT_ROOT / "downloads"
OUTPUT_DIR = PROJECT_ROOT / "downloads_processed"


def convert_xls_to_xlsx(
    input_file: Path,
    output_file: Path,
) -> bool:
    """
    Convert a single OFAC HTML-based .xls file into .xlsx format.

    Parameters
    ----------
    input_file : Path
        Source .xls file.

    output_file : Path
        Destination .xlsx file.

    Returns
    -------
    bool
        True if conversion succeeds, otherwise False.
    """

    try:

        # OFAC .xls files are actually HTML tables.
        tables = pd.read_html(input_file)

        if not tables:
            print(f"[!] No tables found: {input_file.name}")
            return False

        df = tables[0]

        # Replace missing values with empty strings.
        df = df.fillna("")

        df.to_excel(
            output_file,
            index=False,
            engine="openpyxl",
        )

        print(f"[+] Converted: {input_file.name}")

        return True

    except Exception as e:

        print(f"[!] Failed: {input_file.name}")
        print(f"    Error: {e}")

        return False


def process_all_files() -> None:
    """
    Convert all .xls files in the downloads directory.
    """

    if not INPUT_DIR.exists():
        raise FileNotFoundError(
            f"Input directory not found:\n{INPUT_DIR}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    xls_files = sorted(INPUT_DIR.glob("*.xls"))

    if not xls_files:
        print("[!] No .xls files found.")
        return

    converted = 0
    failed = 0

    print("=" * 60)
    print("OFAX XLS to XLSX Converter")
    print("=" * 60)

    for input_file in xls_files:

        output_file = OUTPUT_DIR / f"{input_file.stem}.xlsx"

        success = convert_xls_to_xlsx(
            input_file,
            output_file,
        )

        if success:
            converted += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("Conversion Summary")
    print("=" * 60)

    print(f"Input Files Found : {len(xls_files)}")
    print(f"Converted         : {converted}")
    print(f"Failed            : {failed}")
    print(f"Output Directory  : {OUTPUT_DIR}")

    print("=" * 60)


if __name__ == "__main__":

    process_all_files()