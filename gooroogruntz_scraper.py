#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
import zipfile

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse

from gooroogruntz_scraper_config import GooroogruntzScraperConfig

class GooroogruntzScraper:
    _tasks = list()
    _pages = list()
    _urls = list()

    def __init__(self):
        self._container = os.path.dirname(os.path.realpath(__file__))
        self._config = GooroogruntzScraperConfig()

        if os.path.exists(self._container + '/tmp'):
            shutil.rmtree(self._container + '/tmp')

        os.mkdir(self._container + '/tmp', 0o700)

        if not os.path.exists(self._container + '/loot'):
            os.mkdir(self._container + '/loot', 0o700)

    def add_task(self, task):
        if task not in self._tasks:
            self._tasks.append(task)

    def remove_task(self, task):
        if task in self._tasks:
            self._tasks.remove(task)

    def run(self):
        if not self._tasks:
            self._tasks = ['battlez', 'questz']

        if 'battlez' in self._tasks:
            self.paginate_battlez()
            self.spider_battlez()
            self.scrape_battlez()
            self.package_battlez()
            self.remove_task('battlez')

        if 'questz' in self._tasks:
            self.scrape_questz()

    def paginate_battlez(self, page=None):
        if page is None:
            page = self._config.battlez_urls[0]

        self._pages.append(page)

        soup = self.get_soup(page)
        pagination = soup.find('ul', {'class': ['ui-pagination']})
        next_page = pagination.findChild('li', {'class': 'next'})
        
        if next_page:
            link = next_page.findChild('a', href=True)

            if link:
                self.paginate_battlez(self.get_domain(page) + link['href'])

    def spider_battlez(self):
        for page in self._pages:
            soup = self.get_soup(page)
            domain = self.get_domain(page)
            elements = soup.findAll('tr', {'class': ['item', 'thread']})

            for element in elements:
                if 'announcement' in element['class']:
                    continue

                link = element.findChild('a', {'class': 'thread-link'})
                self._urls.append(domain + link['href'])

    def scrape_battlez(self):
        for url in self._urls:
            soup = self.get_soup(url)
            buttons = soup.findAll('img', {'src': re.compile('Download.gif$', re.I)})

            for button in buttons:
                if button.parent.name == 'a':
                    link = button.parent['href']
                    self.download_file(link)

    def package_battlez(self):
        zip_path = self._container + '/loot/gruntz-' + self.current_task + '.zip'
        amount = 0

        zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

        for root, _, files in os.walk(self._container + '/tmp/' + self.current_task):
            for file in files:
                zip.write(os.path.join(root, file), file)
                amount += 1

        if amount:
            os.rename(zip_path, self._container + '/loot/gruntz-' + self.current_task + '-' + str(amount) + '.zip')
        else:
            os.remove(zip_path)

    def scrape_questz(self):
        print(self._config.questz_urls)

    def download_file(self, url):
        destination_dir = self._container + '/tmp/' + self.current_task

        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir, 0o700)

        parts = urlparse(url)
        destination_name = destination_dir + '/' + os.path.basename(parts.path)
        urlretrieve(url, destination_name)

    @property
    def current_task(self):
        if self._tasks:
            return self._tasks[0]
        return None

    @staticmethod
    def get_domain(url):
        parts = urlparse(url)
        return (parts.scheme + '://'+ parts.netloc)

    @staticmethod
    def get_soup(url):
        try:
            html = urlopen(url)
            soup = BeautifulSoup(html.read(), 'html.parser')
        except HTTPError as err:
            print(err)
            return None
        except URLError as err:
            print(err)
            return None
        else:
            return soup