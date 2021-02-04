# Forked from https://github.com/vittoriotriassi/jobs_scraper/blob/master/jobs_scraper/scraping.py

import requests
import pandas as pd
from time import sleep
from datetime import datetime, timedelta
import random
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

class JobsScraper:
    """JobsScraper is a simple job postings scraper for Indeed."""

    def __init__(self, country: str, position: str, location: str, pages: int, max_delay: int = 0, full_urls: bool = False):
        """
        Create a JobsScraper object.

        Parameters
        ------------
        country: str
            Prefix country. 
            Available countries:
            AE, AQ, AR, AT, AU, BE, BH, BR, CA, CH, CL, CO,
            CZ, DE, DK, ES, FI, FR, GB, GR, HK, HU, ID, IE, 
            IL, IN, IT, KW, LU, MX, MY, NL, NO, NZ, OM, PE, 
            PH, PK, PL, PT, QA, RO, RU, SA, SE, SG, TR, TW, 
            US, VE, ZA.
        position: str
            Job position.
        location: str
            Job location.
        pages: int
            Number of pages to be scraped. Each page contains 15 results.
        max_delay: int, default = 0
            Max number of seconds of delay for the scraping of a single posting.
        full_urls: bool, default = False
            If set to True, it shows the job url column not truncated in the DataFrame.
        """
        if country.upper() == "US":
            self._url = 'https://indeed.com/jobs?q={}&l={}'.format(position, location)
        else:
            self._url = 'https://{}.indeed.com/jobs?q={}&l={}'.format(country, position, location)
        self._country = country
        self._headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        self._pages = pages
        self._max_delay = max_delay
        self._jobs = []
        
        if full_urls:
            pd.set_option('display.max_colwidth', None)
        else:
            pd.reset_option('display.max_colwidth')


    def _extract_page(self, page):

        with requests.Session() as request:
            r = request.get(url="{}&start={}".format(self._url, page), headers=self._headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        return soup


    def _transform_page(self, soup):

        jobs = soup.find_all('div', class_='jobsearch-SerpJobCard')

        for job in jobs:

            try:
                title = job.find(
                    'a', class_='jobtitle').text.strip().replace('\n', '')
            except:
                title = None
            try:
                company = job.find(
                    'span', class_='company').text.strip().replace('\n', '')
            except:
                company = None
            try:
                summary = job.find(
                    'div', {'class': 'summary'}).text.strip().replace('\n', '')
            except:
                summary = None

            if job.find('div', class_='location'):
                try:
                    location = job.find(
                        'div', class_='location').text.strip().replace('\n', '')
                except:
                    location = None
            else:
                try:
                    location = job.find(
                        'span', class_='location').text.strip().replace('\n', '')
                except:
                    location = None
            try:
                href = job.h2.a.get('href')
                if self._country.upper() == "US":
                    job_url = 'https://indeed.com{}'.format(href)
                else:
                    job_url = 'https://{}.indeed.com{}'.format(self._country, href)
            except:
                job_url = None
            try:
                salary = job.find(
                    'span', class_='salary').text.strip().replace('\n', '')
            except:
                salary = None
            try:
                date_posted = job.find(
                    'span', class_='date').text.strip().replace('\n', '')
            except:
                date_posted = None

            job = {
                'title': title,
                'location': location,
                'company': company,
                'summary': summary,
                'salary': salary,
                'date_posted': int(''.join(filter(str.isdigit, date_posted))),
                'date_scraped': datetime.today().strftime("%m/%d/%Y"),
                'url': job_url
            }

            self._jobs.append(job)

            print("Scraping {}...".format(title))

            if self._max_delay > 0:
                sleep(random.randint(0, self._max_delay))
            

    def scrape(self) -> pd.DataFrame:
        """
        Perform the scraping for the parameters provided in the class constructor.
        If duplicates are found, they get dropped.

        Returns
        ------------
        df: pd.DataFrame
            Return a scraped Dataframe.
        """

        for i in tqdm(range(0, self._pages * 10, 10), desc = "Scraping in progress...", total = self._pages):

            page = self._extract_page(i)
            self._transform_page(page)

        df = pd.DataFrame(self._jobs)
        df.drop_duplicates(inplace=True)

        return df