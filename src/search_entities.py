"""
@author : Suprakash Mukherjee

Input file :  ./input/entity_names.csv containing columns : "SLNO" ie; serial number, "NAME"
"""

# selenium webdriver
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import pandas as pd
import re
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path


print("[+] All imports successful..")

# global variables
ofac_sanctions_search = r"https://sanctionssearch.ofac.treas.gov/"
set_download_path = r"/Users/tonystark/Documents/Codebase/Github Codebase/OFAX/downloads/"

def configure_chrome():
    # create download directory if not exists
    if not os.path.exists(set_download_path):
        os.makedirs(set_download_path)

    # configure Chrome options
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-sham-usage')

    # set download preferences
    prefs = {
        "download.default_directory" : set_download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    return driver

def download_data(driver, name, min_name_score):
    ofac_page = ofac_sanctions_search
    driver.get(ofac_page)
    main_window = driver.current_window_handle
    time.sleep(3)

    # # click reset
    # driver.find_element(By.ID, "ctl00_MainContent_btnReset").click()
    # time.sleep(3)

    # enter name
    elem = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.ID, "ctl00_MainContent_txtLastName"))
    )
    elem.clear()
    elem.send_keys(name)

    time.sleep(1)

    # Enter the minimum Score for the search
    # Implemented using Slider

    # Locate Element
    rail = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, "Slider1_railElement"))
    )

    handle = driver.find_element(By.ID, "Slider1_handleImage")

    # get width
    rail_width = rail.size['width']

    # Slider range
    min_val = 50
    max_val = 100
    target = min_name_score

    # calculate offset
    ratio = (target - min_val) / (max_val - min_val)
    offset = int(rail_width * ratio)

    # Move slider (start from leftmost first)
    ActionChains(driver).click_and_hold(handle).move_by_offset(-rail_width, 0).release().perform()

    # Then move to target
    ActionChains(driver).click_and_hold(handle).move_by_offset(offset, 0).release().perform()

    

    # Click Search
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_MainContent_btnSearch"))
    ).click()
    time.sleep(5)

    # click download
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_MainContent_ImageButton1"))
    ).click()

    time.sleep(10)

    return 1

def download_manager(driver, df_input, min_name_score):
    df_sorted = df_input.sort_values(by='SLNO', ascending=True)
    total_count = len(df_sorted)

    for idx, row in enumerate(df_sorted.iterrows(), start=1):
        name = row[1]['NAME']

        try:
            download_data(driver, name, min_name_score)
            print(f"[+] Completed: {idx}/{total_count} -> {name}")
        except Exception as e:
            print(f"[!] Failed: {idx}/{total_count} -> {name} | Error : {e}")
    return driver

def main(df_input, min_name_score):
    print("[+] Initialize OFAC data download..")

    # print(df_input)

    driver = configure_chrome()
    driver = download_manager(driver, df_input, min_name_score)
    driver.quit()
    
    print("[+] Completed all OFAC download successfully !")

    return 1

if __name__ == "__main__":
    # input file
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    input_file = PROJECT_ROOT / "input" / "entity_names.csv"
    df_input = pd.read_csv(input_file)
    
    # print(df_input.head(10))

    # parameters
    min_name_score = 70

    main(df_input, min_name_score)



