import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import os
import datetime
import time
import schedule
import logging

logging.basicConfig(filename='/home/furl/vitalscraper/logs/scrape_cronjob.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

loadtime = 10

columns = ["date", "day", "time", "ppl"]
df = pd.DataFrame(columns=columns)

url = "https://www.vitalclimbinggym.com/brooklyn"
csv_file_path = "/home/furl/vitalscraper/vital_numbers.csv"

def scrape_data():
    try:
        service = Service(executable_path=r"/usr/bin/chromedriver")
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.page_load_strategy = "none"
        
        
        with webdriver.Chrome(options=options) as driver:
            driver.implicitly_wait(5)

            driver.get(url)
            time.sleep(loadtime)

            content = driver.find_element(By.ID, "currocc")
            number_of_people = content.text if content else None

            x = datetime.datetime.now()
            curdate = x.strftime("%Y-%m-%d")
            curtime = x.strftime("%H:%M:%S")
            dayofweek = x.strftime("%A")

            new_row = {"date": curdate, "day": dayofweek, "time": curtime, "ppl": number_of_people}
            # df = df.append(new_row, ignore_index=True)

            # Save data to CSV file after each iteration
            # df.to_csv(csv_file_path, index=False)
            print(number_of_people)
            # print(df)

            if number_of_people:
                return new_row
            else:
                print("number of people is 'none'")
                pass
    except Exception as e:
        logging.exception("Exception occured: ")
        raise
        
def run_scrape_data(df):
    print("Scraping data...")
    new_row = scrape_data()
    df = df._append(new_row, ignore_index=True)
    df.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)
    print("Data scraping complete.")
    
if __name__ == "__main__":
    run_scrape_data(df)
