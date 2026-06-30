"""
------------------------------------------------------------------------------
OFAX - OFAC Search Automation
Author : Suprakash Mukherjee

Description
-----------
Automates searches on the OFAC Sanctions Search website and downloads
the search results for a list of entity names.

Input
-----
./input/entity_names.csv

Required Columns
----------------
SLNO
NAME

Output
------
Downloaded files are saved to:

./downloads/

Project Structure
-----------------
OFAX/
│
├── input/
│   └── entity_names.csv
│
├── downloads/
│
└── src/
    └── search_entities.py
------------------------------------------------------------------------------
"""

import os
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("[+] All imports successful.")

# =============================================================================
# Project Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

INPUT_FILE = PROJECT_ROOT / "input" / "entity_names.csv"
DOWNLOAD_PATH = PROJECT_ROOT / "downloads"

OFAC_URL = "https://sanctionssearch.ofac.treas.gov/"


def configure_chrome():
    """
    Configure Chrome browser.

    The download directory is automatically created if it does not exist.
    """

    DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)

    options = Options()

    # Uncomment for headless execution
    options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.default_directory": str(DOWNLOAD_PATH),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    return driver


def download_data(driver, name, min_name_score):
    """
    Search an entity on the OFAC website and download the search results.
    """

    driver.get(OFAC_URL)

    time.sleep(3)

    # Enter entity name

    elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "ctl00_MainContent_txtLastName")
        )
    )

    elem.clear()
    elem.send_keys(name)

    time.sleep(1)

    # -------------------------------------------------------------------------
    # Configure minimum name score slider
    # -------------------------------------------------------------------------

    rail = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "Slider1_railElement")
        )
    )

    handle = driver.find_element(By.ID, "Slider1_handleImage")

    rail_width = rail.size["width"]

    min_val = 50
    max_val = 100

    ratio = (min_name_score - min_val) / (max_val - min_val)

    offset = int(rail_width * ratio)

    ActionChains(driver) \
        .click_and_hold(handle) \
        .move_by_offset(-rail_width, 0) \
        .release() \
        .perform()

    ActionChains(driver) \
        .click_and_hold(handle) \
        .move_by_offset(offset, 0) \
        .release() \
        .perform()

    # -------------------------------------------------------------------------
    # Execute Search
    # -------------------------------------------------------------------------

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "ctl00_MainContent_btnSearch")
        )
    ).click()

    time.sleep(5)

    # -------------------------------------------------------------------------
    # Download Search Results
    # -------------------------------------------------------------------------

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "ctl00_MainContent_ImageButton1")
        )
    ).click()

    time.sleep(10)

    return 1


def download_manager(driver, df_input, min_name_score):
    """
    Iterate through all entities and download OFAC search results.
    """

    df_sorted = df_input.sort_values(
        by="SLNO",
        ascending=True
    )

    total_count = len(df_sorted)

    for idx, (_, row) in enumerate(df_sorted.iterrows(), start=1):

        name = row["NAME"]

        try:

            download_data(driver, name, min_name_score)

            print(
                f"[+] Completed: {idx}/{total_count} -> {name}"
            )

        except Exception as e:

            print(
                f"[!] Failed: {idx}/{total_count} -> {name} | Error: {e}"
            )

    return driver


def main(df_input, min_name_score):
    """
    Main execution function.
    """

    print("[+] Initializing OFAX...")

    driver = configure_chrome()

    try:

        download_manager(
            driver,
            df_input,
            min_name_score
        )

    finally:

        driver.quit()

    print("[+] Completed all OFAC downloads successfully.")

    return 1


if __name__ == "__main__":

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{INPUT_FILE}"
        )

    df_input = pd.read_csv(INPUT_FILE)

    MIN_NAME_SCORE = 70

    main(df_input, MIN_NAME_SCORE)