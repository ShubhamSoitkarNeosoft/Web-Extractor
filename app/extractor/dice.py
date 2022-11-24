
import random
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree


class ExtractIndeed:

    BASE_URL = 'https://in.indeed.com'
    FILE_NAME = 'indeed_jobs_python.csv'

    def __init__(self, language):
        # instantiate a chrome options object so you can set the size and headless preference
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.language = language.lower()
        self.job_detail_links = []

  

    def get_job_detail_links(self):
        for page in range(1, 2):
            query_param = f'{self.language}-jobs'
            time.sleep(5)
            URL = f"https://www.dice.com/jobs?q={self.language}&page={page}"
            self.driver.get(URL)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            a = soup.findAll('a',class_='card-title-link bold')
            time.sleep(5)
            print(a)
            # for i in a:
            #     print(i[0])
            # print(a)
            # soup = BeautifulSoup(webpage.content, "html.parser")
            dom = etree.HTML(str(soup))
            print('-------',dom.xpath('//div[@class="card-company"]/a'))
            
            # for outer_artical in soup.findAll(attrs={'class': "card-title-link bold"}):
            #     print('****',outer_artical)
                
                # for inner_links in outer_artical.findAll(attrs={'class': "jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0"}):
                #     self.job_detail_links.append(
                #         f"{self.BASE_URL}{inner_links.a.get('href')}")

    def scrap_details(self):
        self.get_job_detail_links()
        time.sleep(2)
        description_list, company_name_list, designation_list, salary_list, company_url = [], [], [], [], []
        location_list, qualification_list= [],[]

        # for link in range(len(self.job_detail_links)):

        #     time.sleep(5)
        #     self.driver.get(self.job_detail_links[link])
        #     soup = BeautifulSoup(self.driver.page_source, 'lxml')
            

    # def save_to_csv(self):
    #     self.scrap_details()
        # df = pd.DataFrame()
        # df['Company Name'] = company_name_list
        # df['Company_url'] = company_url
        # df['salary'] = salary_list
        # # df['description_list'] = description_list
        # df['designation_list'] = designation_list
        # df['location_list'] = location_list
        # df['qualification_list'] = qualification_list
        # df.to_csv(self.FILE_NAME, index=False)
        

scrap_naukri = ExtractIndeed('python')
scrap_naukri.scrap_details()






