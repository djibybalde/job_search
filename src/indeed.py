# -*- coding: utf-8 -*-

"""
    Scripts to search and scrape jobs on https://fr.indeed.com
"""

import os
import yaml
import time
import numpy as np
import pandas as pd
from termcolor import colored

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

ENV_FILE = os.path.join(os.getcwd().split('job_search')[0], 'job_search', 'env.yaml')
with open(ENV_FILE) as yf:
    params = yaml.load(yf, Loader=yaml.FullLoader)

# Directories initialisation
ROOT_DIR = os.path.dirname(os.path.abspath(ENV_FILE))
DRIVER_PATH = os.path.join(ROOT_DIR, params['directories']['driver_dir'], params['files']['driver_path'])
OUTPUT_PATH = os.path.join(ROOT_DIR, params['directories']['scraped'])

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)


def timer(t1=1, t2=2):
    return np.random.uniform(t1, t2)


def params(email: str = '', pwd: str = None) -> tuple:
    """
    Information to connect to the website.

    Args:
        email (str): Your e-mail address to connect to the website
        pwd (str): Your password to connect to the website
    Return:
        A tuple object containing your e-mail and password
    """

    print(' ')
    if email is None or email == '':
        email = input(colored('Enter your E-mail address here: ', 'green'))

    if pwd is None or pwd == '':
        pwd = input(colored('Enter your password here: ', 'green'))

    return email, pwd


class JobFinder:
    """
    Search and scrape job from fr.indeed.com
    """

    def __init__(self,
                 user_params: tuple = params(),
                 job_title: str = 'data scientist',
                 location: str = 'france',
                 job_type: str = 'cdi',
                 length: int = 10,
                 ):
        """
        Parameters initialisation

        Args:
            user_params (tuple): Your email (address, password) respectively
            job_title (str): What is your favorite job title or keyword ?
            location (str): Where do you want to apply the for job ?
            job_type (str): Which type of job are you looking for ?
            length (str): How many example of job do you want to apply ?

        """

        self.driver_path = DRIVER_PATH
        print(self.driver_path)
        self.email, self.password = user_params
        self.job_title = job_title.lower()
        self.job_type = job_type.lower()
        self.location = location.capitalize()
        self.length = int(length)

        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=webdriver.ChromeOptions())

        self.excludes = ['stage', 'stagiaire', 'internship', 'apprentissage', ' contrat pro', 'alternance',
                         'alternance/stage', 'stage/alternance', '(alternance/stage)', '(stage/alternance)',
                         'intern', '[stage]', '[alternance]', '(alternance)', '(stage)',
                         'lead', 'senior', 'confirmé', 'expert', 'expérimenté', 'chef', 'Chief', ]

    def login(self):

        """
        Login into fr.indeed.com
        """
        self.driver.set_window_size(width=1000, height=900)  # maximize_window()
        self.driver.get('https://fr.indeed.com')

        print(f"\nLogin into {colored('https://fr.indeed.com', 'blue')} ...")
        time.sleep(timer(1, 2))
        self.driver.find_element_by_class_name('gnav-LoggedOutAccountLink-text').click()

        time.sleep(timer(1, 2))
        email = self.driver.find_element_by_id('login-email-input')
        email.clear()
        email.send_keys(self.email)

        time.sleep(timer(1, 2))
        password = self.driver.find_element_by_id('login-password-input')
        password.clear()
        password.send_keys(self.password)

        time.sleep(timer(2, 3))
        password.send_keys(Keys.RETURN)

    def search(self):
        """
        Searching for jobs
        """

        print(f"Searching for {colored(self.job_title.capitalize(), 'blue')} job ...")
        time.sleep(timer(1, 2))
        keywords = self.driver.find_element_by_id("text-input-what")
        keywords.click()
        keywords.clear()
        keywords.send_keys(self.job_title)

        time.sleep(timer(1, 2))
        location = self.driver.find_element_by_id("text-input-where")
        location.send_keys(len(location.get_attribute('value')) * Keys.BACK_SPACE)
        location.send_keys(self.location)
        location.send_keys(Keys.RETURN)

        time.sleep(timer(1, 2))
        self.driver.find_element_by_id("filter-job-type").click()

        if self.job_title.lower() is 'data science':
            job_type = '5' if self.job_type == 'cdi' else '7'

        elif self.job_title.lower() is 'data scientist':
            job_type = '1' if self.job_type == 'cdi' else '5'

        elif self.job_title.lower() is 'data analyst':
            job_type = '2' if self.job_type == 'cdi' else '7'

        else:  # self.job_title.lower() in ['data analyse', 'statistique', 'statisticien']:
            job_type = '2' if self.job_type == 'cdi' else '4'

        job_type = f"//*[@id='filter-job-type-menu']/li[{job_type}]"
        self.driver.find_element_by_xpath(job_type).click()

        time.sleep(timer(1, 2))
        button_x = self.driver.find_element_by_id("popover-x")
        button_x.click()

        time.sleep(timer(1, 2))
        cookies = self.driver.find_element_by_id("onetrust-accept-btn-handler")
        cookies.click()

        try:
            self.driver.find_element_by_xpath("//*[@id='filter-dateposted']/button").click()
            time.sleep(timer(0, 1))
            self.driver.find_element_by_xpath("//*[@id='filter-dateposted']/button").click()
            time.sleep(timer(0, 1))
            self.driver.find_element_by_xpath("//*[@id='filter-dateposted-menu']/li[2]").click()

        except NoSuchElementException:
            pass

    def scrape(self):
        """
        Jobs scraper
        """

        page = 0
        jobs = list()

        print(f"Scraping {colored(self.job_title.capitalize(), 'blue')} jobs ...")
        while len(jobs) < self.length:
            count = 0
            print(f' - Scraping in page {1 + page} ... ')

            current_page = self.driver.page_source
            soup = BeautifulSoup(current_page, "lxml")
            jobs_container = soup.find(id="resultsCol")

            for job in jobs_container.find_all('div', class_='jobsearch-SerpJobCard'):

                title_ref = job.find('h2', class_="title").text.strip()
                if all(exclude not in title_ref.lower().split() for exclude in self.excludes):

                    title = ' '.join([t for t in title_ref.split() if t != 'nouveau'])
                    company = job.find('span', class_='company').text.strip()
                    link = "https://fr.indeed.com" + job.find('a').get("href")

                    if job.find('span', class_='date') is not None:
                        date = job.find('span', class_='date').text.strip()
                    else:
                        date = job.find('div', class_='date').text.strip()

                    if job.find('span', class_="location accessible-contrast-color-location") is not None:
                        location = job.find('span', class_="location accessible-contrast-color-location").text.strip()
                    else:
                        location = job.find('div', class_="location accessible-contrast-color-location").text.strip()

                    # Save it
                    jobs.append({'Title': title, 'Company': company, 'Location': location, 'Date': date, 'Link': link})

                count += 1
                if len(jobs) >= self.length:
                    break

            print(f' - Found: {count} ==> total: {len(jobs)} ')

            # Next page
            page += 1
            try:
                time.sleep(timer(3, 5))
                self.driver.find_element_by_xpath(f"//*[@id='resultsCol']/nav/div/ul/li[{page}]/a").click()
            except NoSuchElementException:
                pass

        # Ignore the duplicated data
        df = pd.DataFrame(jobs).drop_duplicates(ignore_index=True)
        template = colored('Found {} {} unique jobs (no-duplicated).', 'green')
        print(template.format(df.shape[0], self.job_title.capitalize()))

        # Write to a Excel file
        MY_FILE_NAME = ''.join([OUTPUT_PATH, ''.join(self.job_title.split()), '.xlsx'])
        df.to_excel(MY_FILE_NAME)
        print(colored(f'Your data are written in {MY_FILE_NAME}', 'green'))

        # Close the driver
        self.driver.quit()

    def get_results(self):
        self.login()
        self.search()
        self.scrape()


if __name__ == '__main__':
    JobFinder(job_title='data science', location='france', length=50, ).get_results()
