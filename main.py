from keboola.component import CommonInterface
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time
import logging
import csv
import os
import io


if __name__ == "__main__":
    ci = CommonInterface()
    params = ci.configuration.parameters

    username = params["username"]
    password = params["#password"]

    logging.info(f"Username: {username}")
    list_of_downloads = []

    with open('/data/in/tables/emails.csv') as emails_table:
        emails = csv.DictReader(emails_table)
        for email in emails:
            list_of_downloads.append(email['download_url'])

    if len(list_of_downloads) == 0:
        logging.error("No reports to be downloaded. JOB will terminate")
        exit(1)
    elif len(list_of_downloads) > 1:
        logging.info("There is more than 1 report to be downloaded. Only the most recent one will be processed")

    url_to_download = list_of_downloads[-1]

    logging.info(f"The URL of the report to be downloaded is: {url_to_download}")

    logging.info("Starting the selenium process to download the report")

    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory": "/data/out/tables/"}

    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": r"/data/out/tables/",  ### Set the path accordingly
             "download.prompt_for_download": False,  ## change the downpath accordingly
             "download.directory_upgrade": True}

    # driver = webdriver.Chrome(options=chrome_options)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("prefs", prefs)


    driver = webdriver.Chrome(options=chrome_options)

    # driver = webdriver.Chrome()
    driver.get(url_to_download)

    username_field = driver.find_element(By.XPATH, "//*[@id=\"mainContainer\"]/div/div/div/div/app-login/div[2]/div[3]/div/form/div[1]/input")
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.XPATH, "//*[@id=\"mainContainer\"]/div/div/div/div/app-login/div[2]/div[3]/div/form/div[2]/input")
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


    time.sleep(60)


    response = requests.get(url_to_download).content.decode('utf-8')
    # df = pd.read_csv(io.StringIO(response.decode('utf-8')))
    # df.to_csv(f'/data/out/tables/GlobalReport.csv', encoding='utf-8', index=False)

    cr = csv.reader(response.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)
    driver.get("chrome://downloads/")

    print(os.getcwd())
    os.chdir("/data/out/tables/")
    print(os.getcwd())
    print(os.listdir())











