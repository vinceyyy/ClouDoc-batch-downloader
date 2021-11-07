# used for batch downloading files from ClouDoc while maintaining the same folder structure
# to use:
# 1. setup webdriver for chrome: https://chromedriver.chromium.org/downloads
# 2. change webdriver_path to your downloaded chrome driver
# 3. change targets = pairs of ClouDoc url and password (if no password requried, just leave a empty string)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from pprint import pprint
import requests
import os


webdriver_path = "./chromedriver"
local_path = "./downloads"
targets = [("url", "password")]

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)


def go_back():
    r = [
        folder
        for folder in driver.find_elements(By.CSS_SELECTOR, ".folder-name")
        if folder.text == "Return"
    ][0]
    r.click()


def get_folder_sturcture(output):
    #  for a given page, download all files on this page, create local folders for each folder, enter and repeat (recursive)
    # current path
    remote_path = driver.find_element(By.CSS_SELECTOR, ".file-directory").get_attribute(
        "title"
    )

    # get all files
    elems = driver.find_elements(By.CSS_SELECTOR, ".external-btn.file-download")
    file_elems = [elem for elem in elems if elem.text == "Download"]
    files = [
        {
            "name": f.find_element(By.XPATH, "../..").text.split("\n")[0],
            "link": f.get_attribute("href"),
        }
        for f in file_elems
    ]
    output[remote_path] = files

    # loop through all folders
    folders = [
        folder
        for folder in driver.find_elements(By.CSS_SELECTOR, ".folder-name")
        if folder.text not in ["Root Folder", "Return", ""]
    ]
    # if no subfolder, return
    if not folders:
        go_back()
    else:
        for index, folder in enumerate(folders):
            # html elements are re-generated after each click, so we need to find the element again
            new_folder = [
                folder
                for folder in driver.find_elements(By.CSS_SELECTOR, ".folder-name")
                if folder.text not in ["Root Folder", "Return", ""]
            ][index]
            name = new_folder.text
            print("folder scanned: " + remote_path + "/" + name)
            new_folder.click()
            sleep(1)
            get_folder_sturcture(output=output)
            go_back()
            sleep(1)


def process_one_url(url: str, password: str):
    output = {}
    driver.get(url)
    if len(password) > 0:
        pwd = driver.find_element(By.CSS_SELECTOR, ".pwd-input")
        pwd.send_keys(password)
        pwd.send_keys(Keys.RETURN)
        sleep(3)
    get_folder_sturcture(output=output)
    print("Start downloading...")
    for folder, files in output.items():
        for _file in files:
            file_path = local_path + folder + "/" + _file["name"]
            print("downloading: " + file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(requests.get(_file["link"]).content)


for (url, password) in targets:
    process_one_url(url, password)
    print(url + " finished")
