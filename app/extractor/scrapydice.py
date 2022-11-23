
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import time

with open('job_scraping.csv','w') as file:
    file.write("Job_Title\n")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://www.dice.com/jobs')

driver.maximize_window()
time.sleep(3)

job_title = driver.find_element(By.ID, "typeaheadInput")
job_title.click()
job_title.send_keys("Python")
time.sleep(3)

job_location = driver.find_element(By.ID, "google-location-search")
job_location.click()
job_location.send_keys("Pune")
time.sleep(3)

search = driver.find_element(By.ID, "submitSearch-button")
search.click()

time.sleep(2)

job_titles =  driver.find_elements(By.CLASS_NAME, "card-title-link")

# for title in job_titles:
#     print(title.text)

company_name = driver.find_elements(By.XPATH,'//div[@class="card-company"]/a')

# for company in company_name:
#     print(company.text)

job_locations =  driver.find_elements(By.CLASS_NAME, "search-result-location")

# for location in job_locations:
#     print(location.text)

job_types = driver.find_elements(By.XPATH,'//div[@class="card-position-type"]/span')

# for job_type in job_types:
#     print(job_type.text)

job_posted_dates = driver.find_elements(By.CLASS_NAME, "posted-date")

# for posted_date in job_posted_dates:
#     print(posted_date.text)


job_modified_dates = driver.find_elements(By.CLASS_NAME, "modified-date")

# for modified_date in job_modified_dates:
#     print(modified_date.text)

job_descriptions = driver.find_elements(By.CLASS_NAME, "card-description")

# for description in job_descriptions:
#     print(description.text)


with open('job_scraping.csv','a') as file:
    for i in range(len(job_titles)):
        file.write(job_titles[i].text + ',' + job_modified_dates[i].text + ',' + company_name[i].text + ',' + job_locations[i].text + ',' + job_posted_dates[i].text + ',' + job_descriptions[i].text +"\n")
