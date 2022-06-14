import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from common.config import config
from pathlib import Path
from datetime import datetime

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_prefs = {"download.default_directory": config.download_dir}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

browser = webdriver.Chrome(options=set_chrome_options())
browser.implicitly_wait(1)

def get_downloaded_files():
    return Path(config.download_dir).glob('**/*')

def download_data():
    """Download the dataset using selenium """
    host = os.getenv("DATA_HOST")
    user = os.getenv("DATA_USER")
    pswd = os.getenv("DATA_PASSWORD")

    before = get_downloaded_files()

    # site login
    browser.get(host)
    username = browser.find_element(By.ID, "login-input-email")
    password = browser.find_element(By.ID, "login-input-password")
    username.send_keys(user)
    password.send_keys(pswd)

    # navigate to download
    login_button = '//*[@id="login-submit"]/button'
    delay_popup = '//*[@id="delay-info"]'
    clickflow = [
        # list view
        '//*[@id="split-screen-buttons"]/button[1]',
        # portfolio
        '//*[@id="tour-list-buttons"]/button[3]',
        # # valuation view
        # '//*[@id="workspace"]/div[2]/div[4]/div/button[2]',
        # sharing dropdown
        '//*[@id="workspace"]/div[2]/div[1]/div/div[5]/button',
        # export data
        '//*[@id="workspace"]/div[2]/div[1]/div/div[5]/ul/li[1]',
        # export button
        '//*[@id="export-options-dlg-ok-btn"]'
    ]

    browser.find_element(By.XPATH, login_button).click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, clickflow[0])))
    WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.XPATH, delay_popup)))

    for idx in range(len(clickflow)):
        browser.get_screenshot_as_file(config.screenshot_dir + "/screenshot.png")
        browser.find_element(By.XPATH, clickflow[idx]).click()
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, clickflow[idx+1])))
        except (ElementNotInteractableException, IndexError):
            pass
    
    most_recent = 0
    for file in get_downloaded_files():
        if (time:=file.stat().st_mtime) >= most_recent:
            most_recent = time
            filepath = file

    dowload_date = datetime.utcfromtimestamp(most_recent).strftime('%Y-%m-%d %H:%M:%S')
    
    return filepath, dowload_date


if __name__ == "__main__":
    download_data()
