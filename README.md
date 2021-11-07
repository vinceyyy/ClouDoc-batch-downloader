# ClouDoc-batch-downloader

My company uses ClouDoc as private cloud but does not keep it up to date. The downloading folder feature is broken, iOS app is not supported by the current iOS version, and I cannot get the desktop client to work as well.

In this scenario, downloading dozens of nested folders from ClouDoc while maintaining the file structure is the most tipical pain-in-the-butt intern job. I was that intern. So I made this.

This project runs a headless chrome webdriver via `selenium` to recursively walk thru all the folders and subfolders, record all files and their path, then pass it to `requests` to download.

## To Use

1. install selenium and requests.
2. download chrome webdriver from https://chromedriver.chromium.org/downloads and put the path of executable to `webdriver_path`.
3. add ClouDoc url and password (is applicable) to `targets` as list of tuples.
4. `python3 main.py`
