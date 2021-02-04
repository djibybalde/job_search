# -*- coding: utf-8 -*-

""" Scripts to search and scrape jobs on https://fr.indeed.com """

import os
import time
import yaml
import json
import numpy as np
import pandas as pd
from termcolor import colored
from nltk.tokenize import word_tokenize

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Yaml file to get directories/paths
ENV_FILE = os.path.join(os.getcwd().split('job_search')[0], 'job_search', 'env.yaml')
with open(ENV_FILE) as yf:
    PARAMS = yaml.load(yf, Loader=yaml.FullLoader)

# Directories initialisation
ROOT_DIR = os.path.dirname(os.path.abspath(ENV_FILE))
DRIVER_PATH = os.path.join(ROOT_DIR, PARAMS['directories']['driver_dir'], PARAMS['files']['driver_path'])
FILTER_FILE = os.path.join(ROOT_DIR, PARAMS['directories']['data_dir'], PARAMS['files']['filter_word'])
OUTPUT_PATH = os.path.join(ROOT_DIR, PARAMS['directories']['job_data'])

# Make an output path
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)


def timer(t1=1, t2=2):
    """ Return a random number between t1 and t2"""
    return np.random.uniform(t1, t2)


def read_json(path: str):
    """ Read a JSON file """
    with open(path, mode='r') as file:
        return json.loads(file.read())


def params(email: str = '', pwd: str = None) -> tuple:
    """
    Information to connect to the website.

    Args:
        email (str): Your e-mail address to connect to the website
        pwd (str): Your password to connect to the website
    Return:
        A tuple object containing your e-mail and password
    """

    if email is None or email == '':
        email = input(colored('Enter your E-mail address here: ', 'green'))

    if pwd is None or pwd == '':
        pwd = input(colored('Enter your password here: ', 'green'))

    return email, pwd


class JobFinder:

    """ Search and scrape job from https://fr.indeed.com website """

    def __init__(self,
                 login: bool = False,
                 job_title: str = 'data science',
                 location: str = 'france',
                 job_type: str = 'cdi',
                 max_numb: int = 20,
                 ):
        """
        Parameters initialisation

        Args:
            login (bool): Whether to login with your email and password on the website.
            job_title (str): What job are you looking for ?
            job_type (str): What type of job are you looking for e.g. CDI, CDD ?
            location (str): Where do you want to apply for job ?
            max_numb (str): How many example of job do you want to apply ?

        """

        self.log_in = login
        self.email, self.password = params() if self.log_in else '', ''

        self.job_title = job_title.lower()
        self.job_type = job_type.lower()
        self.location = location.capitalize()
        self.max_numb = int(max_numb)

        self.excludes = read_json(FILTER_FILE)['excludes']
        self.includes = read_json(FILTER_FILE)['includes']

        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=webdriver.ChromeOptions())

    def login(self):

        """ Login into fr.indeed.com website """

        self.driver.set_window_size(width=1000, height=900)  # maximize_window()
        self.driver.get('https://fr.indeed.com')
        time.sleep(timer(1, 2))

        if self.log_in:
            print(f"\nLogin into {colored('https://fr.indeed.com', 'blue')} ...")
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

    def search(self, select_type: bool = False):

        """ Searching for jobs """

        # Open https://fr.indeed.com in the Google Chrome browser and login.
        print(' ')
        self.login()
        time.sleep(timer(1, 2))
        template = "Searching for {} job in {} ..."
        print(template.format(colored(self.job_title.capitalize(), 'blue'), colored(self.location, 'blue')))

        # What kind of job are you for ?
        keywords = self.driver.find_element_by_id("text-input-what")
        keywords.click()
        keywords.clear()
        keywords.send_keys(self.job_title)
        time.sleep(timer(1, 2))

        # Where do want to apply for job ?
        location = self.driver.find_element_by_id("text-input-where")
        location.send_keys(len(location.get_attribute('value')) * Keys.BACK_SPACE)
        location.send_keys(self.location)
        location.send_keys(Keys.RETURN)
        time.sleep(timer(2, 3))

        # Accept the cookies
        cookies = self.driver.find_element_by_id("onetrust-accept-btn-handler")
        cookies.click()
        time.sleep(timer(1, 2))

        # Select the publication date
        self.driver.find_element_by_id("filter-dateposted").click()
        self.driver.find_element_by_xpath("//*[@id='filter-dateposted']/button").click()
        self.driver.find_element_by_xpath("//*[@id='filter-dateposted-menu']/li[2]").click()
        time.sleep(timer(1, 2))

        # Close the popup window: appear when the page is refresh
        button_x = self.driver.find_element_by_id("popover-x")
        button_x.click()
        time.sleep(timer(1, 2))

        # Select job type (CDI, CDD, internship, ...)
        if select_type:
            self.driver.find_element_by_id("filter-job-type").click()

            if self.job_title is 'data science':
                job_type = '5' if self.job_type == 'cdi' else '7'
            elif self.job_title is 'data scientist':
                job_type = '1' if self.job_type == 'cdi' else '5'
            elif self.job_title is 'data analyst':
                job_type = '2' if self.job_type == 'cdi' else '7'
            else:
                job_type = '2' if self.job_type == 'cdi' else '4'

            job_type = f"//*[@id='filter-job-type-menu']/li[{job_type}]"
            self.driver.find_element_by_xpath(job_type).click()
            time.sleep(timer(1, 2))

    def scrape(self):

        """ Jobs scraper """

        page = 0
        jobs = list()

        template = "Scraping {} job in {} ..."
        print(template.format(colored(self.job_title.capitalize(), 'blue'), colored(self.location, 'blue')))

        while len(jobs) < self.max_numb:
            count = 0
            print(' - Scraping in page {} ... '.format(1 + page))

            current_page = self.driver.page_source
            soup = BeautifulSoup(current_page, "lxml")
            jobs_container = soup.find(id="resultsCol")

            for job in jobs_container.find_all('div', class_='jobsearch-SerpJobCard'):

                title_ref = job.find('h2', class_="title").text.strip()
                if all(word not in word_tokenize(title_ref.lower(), language='french') for word in self.excludes):

                    link = "https://fr.indeed.com" + job.find('a').get("href")
                    title = ' '.join([w for w in title_ref.split() if w != 'nouveau'])
                    company = job.find('span', class_='company').text.strip()

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
                if len(jobs) >= self.max_numb:
                    break

            # Next page
            page += 1
            try:
                time.sleep(timer(3, 5))
                self.driver.find_element_by_xpath(f"//*[@id='resultsCol']/nav/div/ul/li[{page}]/a").click()
            except NoSuchElementException:
                pass

        # Ignore the duplicated data and write to a Excel file
        if all(n in word_tokenize(self.job_title, language='french')
               for n in word_tokenize("chargé d'études statistiques", language='french')):
            NAME = 'Statistiques'
        else:
            NAME = ''.join(word.capitalize() for word in self.job_title.split())

        df = pd.DataFrame(jobs).drop_duplicates(ignore_index=True)
        template = colored('According to your search criteria, there are {} {} jobs available in {}', 'cyan')
        print(template.format(df.shape[0], NAME, self.location, ))

        FILE_LOC = ''.join([OUTPUT_PATH, NAME, '.xlsx'])
        df.to_excel(FILE_LOC)
        print(f"This data are written in {colored(FILE_LOC, 'cyan')}")

        # Close the driver
        self.driver.quit()

    def get_results(self):
        self.search(select_type=False)
        self.scrape()


if __name__ == '__main__':
    JobFinder(login=False, job_title='data scientist', location='france', max_numb=50, ).get_results()
