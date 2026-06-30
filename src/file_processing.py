"""
------------------------------------------------------------------------------
OFAX - OFAC Search Automation
Author : Suprakash Mukherjee
"""

import os
import pandas as pd

# input and output folders
INPUT_DIR = "./downloads"
OUTPUT_DIR = "./downloads_processed"

# create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_xls_to_xlsx(file_path, output_path):
    try:
        # read as HTML (since the .xls files are HTML-based)
        tables = pd.read_html(file_path)

        if not tables:
            print(f"[-] No tables found in {file_path}")
            return
        
        # take first table
        df = tables[0]

        # Optional cleanup
        df = df.fillna("")

        # save as xlsx
        df.to_excel(output_path, index=False, engine="openpyxl")

        print(f"[+] Converted: {file_path} -> {output_path}")
    except Exception as e:
        print(f"[-] Failed: {file_path}")
        print(f"[-] Error: {e}")


def process_all_files():
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".xls"):
            input_file = os.path.join(INPUT_DIR, file)

            # replace extension with .xlsx
            output_file_name = os.path.splitext(file)[0] + ".xlsx"
            output_file_name = os.path.join(OUTPUT_DIR, output_file_name)

            convert_xls_to_xlsx(input_file, output_file_name)


if __name__ == "__main__":
    process_all_files()