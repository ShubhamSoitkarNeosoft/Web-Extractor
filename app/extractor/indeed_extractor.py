
import random
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class ExtractIndeed:

    BASE_URL = 'https://in.indeed.com'
    FILE_NAME = 'indeed_jobs_python.csv'

    def __init__(self, language):
        # instantiate a chrome options object so you can set the size and headless preference
        options = webdriver.ChromeOptions()
        # options = Options()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--incognito')
        options.add_argument('--headless')
        # options.add_argument("--window-size=1920x1080")
        # options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver_exc = 'chromedriver'
        # self.driver = webdriver.Chrome(driver_exc, options=options)
        self.language = language.lower()
        self.job_detail_links = []

  

    def get_job_detail_links(self):
        for page in range(0, 1):
            query_param = f'{self.language}-jobs'
            time.sleep(5)
            URL = f"https://in.indeed.com/jobs?q={self.language}&start={page*10}"
            self.driver.get(URL)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            for outer_artical in soup.findAll(attrs={'class': "css-1m4cuuf e37uo190"}):
                for inner_links in outer_artical.findAll(attrs={'class': "jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0"}):
                    self.job_detail_links.append(
                        f"{self.BASE_URL}{inner_links.a.get('href')}")

    def scrap_details(self):
        self.get_job_detail_links()
        time.sleep(2)
        description_list, company_name_list, designation_list, salary_list, company_url = [], [], [], [], []
        location_list, qualification_list= [],[]

        for link in range(len(self.job_detail_links)):

            time.sleep(5)
            self.driver.get(self.job_detail_links[link])
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            a = soup.findAll(
                attrs={'class': "jobsearch-InlineCompanyRating-companyHeader"})
            company_name_list.append(a[1].text)
            try:
                company_url.append(a[1].a.get('href'))
            except:
                company_url.append('NA')

            salary = soup.findAll(
                attrs={'class': "jobsearch-JobMetadataHeader-item"})
            if salary:
                for i in salary:
                    x = i.find('span')
                    if x:
                        salary_list.append(x.text)
                    else:
                        salary_list.append('NA')
            else:
                salary_list.append('NA')

            description = soup.findAll(
                attrs={'class': "jobsearch-jobDescriptionText"})
            # description_list.append(description.string)
            if description:
                for i in description:
                    description_list.append(i.text)
            else:
                description_list.append('NA')
            # print(len(description_list), len(company_url), len(salary_list))

            designation = soup.findAll(attrs={'class':'jobsearch-JobInfoHeader-title-container'})
            if designation:
                designation_list.append(designation[0].text)
            else:
                designation_list.append('NA')

            #location

            for Tag in soup.find_all('div', class_="icl-Ratings-count"):
                Tag.decompose()
            for Tag in soup.find_all('div', class_="jobsearch-CompanyReview--heading"):
                Tag.decompose()
            location = soup.findAll(attrs={'class':"jobsearch-CompanyInfoWithoutHeaderImage"})
            if location:
                for i in location:
                    location_list.append(i.text)
            else:
                location_list.append('NA')

            #Qualification
            qualification = soup.findAll(attrs={"class":'jobsearch-ReqAndQualSection-item--wrapper'})
            if qualification:
                for i in qualification:
                    qualification_list.append(i.text)
            else:
                qualification_list.append('NA')
        job_data = {
                'company_name':company_name_list,
                'location':location_list
            }  
        return job_data   
        
        # return  company_name_list, designation_list, salary_list, company_url,location_list, qualification_list

    # def save_to_csv(self):
    #     self.scrap_details()
    #     df = pd.DataFrame()
    #     df['Company Name'] = company_name_list
    #     df['Company_url'] = company_url
    #     df['salary'] = salary_list
    #     # df['description_list'] = description_list
    #     df['designation_list'] = designation_list
    #     df['location_list'] = location_list
    #     df['qualification_list'] = qualification_list
    #     df.to_csv(self.FILE_NAME, index=False)



