from keboola.component import CommonInterface
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging
import csv

if __name__ == "__main__":
    ci = CommonInterface()
    params = ci.configuration.parameters

    username = params["username"]
    password = params["#password"]

    logging.info(f"Username: {username}")

    with open('/in/tables/emails.csv') as emails_table:
        emails = csv.DictReader(emails_table)
        for email in emails:
            print(email['ui'], email['body_html'])

