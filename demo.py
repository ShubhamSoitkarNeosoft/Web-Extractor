
import random
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class ScrapNaukriJobs:

    BASE_URL = 'https://in.indeed.com'
    FILE_NAME = 'scrap_indeed_jobs_ui_ux.csv'

    def __init__(self, language):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
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
        description_list, company_name_list, experience_list, salary_list, company_url = [], [], [], [], []

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

            salary = soup.findAll(attrs={'class':"jobsearch-JobMetadataHeader-item"})
            if salary:
                for i in salary:
                        x = i.find('span')
                        if x:
                            salary_list.append(x.text)
                        else:
                            salary_list.append('NA')
            else:
                salary_list.append('NA')

            description = soup.findAll(attrs={'class':"jobsearch-jobDescriptionText"})
            # description_list.append(description.string)
            if description:
                for i in description:
                    description_list.append(i.text)
            else:
                description_list.append('NA')
            print(len(description_list),len(company_url),len(salary_list))
            

        # df = pd.DataFrame()
        # df['Company Name'] = company_name_list
        # df['Company_url'] = company_url
        # df['salary'] = salary_list
        # df['description_list']= description_list
        # df.to_csv(self.FILE_NAME, index=False)


if __name__ == "__main__":
    scrap_naukri = ScrapNaukriJobs("python")
    scrap_naukri.scrap_details()
