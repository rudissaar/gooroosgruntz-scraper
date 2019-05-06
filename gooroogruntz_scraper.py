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

    def process_task(self, task):
        self._pages.clear()
        self._urls.clear()

        self.paginate(task)
        self.spider(task)
        self.scrape(task)
        self.package(task)

    def run(self):
        if not self._tasks:
            self._tasks = ['battlez', 'questz']

        for task in self._tasks:
            self.process_task(task)

    def paginate(self, task, page=None):
        if page is None:
            page = getattr(self._config, task + '_urls').pop(0)

        self._pages.append(page)

        soup = self.get_soup(page)
        pagination = soup.find('ul', {'class': ['ui-pagination']})
        next_page = pagination.findChild('li', {'class': 'next'})
        
        if next_page:
            link = next_page.findChild('a', href=True)

            if link:
                self.paginate(task, self.get_domain(page) + link['href'])
            elif not link and getattr(self._config, task + '_urls'):
                self.paginate(task)

    def spider(self, task):
        for page in self._pages:
            soup = self.get_soup(page)
            domain = self.get_domain(page)
            elements = soup.findAll('tr', {'class': ['item', 'thread']})

            for element in elements:
                if 'announcement' in element['class']:
                    continue

                link = element.findChild('a', {'class': 'thread-link'})
                self._urls.append(domain + link['href'])

    def scrape(self, task):
        for url in self._urls:
            soup = self.get_soup(url)
            buttons = soup.findAll('img', {'src': re.compile('Download.gif$', re.I)})

            for button in buttons:
                if button.parent.name == 'a':
                    link = button.parent['href']
                    pattern = re.compile('.wwd$', re.I)

                    if pattern.search(urlparse(link).path):
                        self.download_file(task, link)

    def package(self, task):
        zip_path = self._container + '/loot/gruntz-' + task + '.zip'
        amount = 0

        zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

        for root, _, files in os.walk(self._container + '/tmp/' + task):
            for file in files:
                zip.write(os.path.join(root, file), file)
                amount += 1

        if amount:
            os.rename(zip_path, self._container + '/loot/gruntz-' + task + '-' + str(amount) + '.zip')
        else:
            os.remove(zip_path)

    def download_file(self, task, url):
        destination_dir = self._container + '/tmp/' + task

        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir, 0o700)

        parts = urlparse(url)
        destination_name = destination_dir + '/' + os.path.basename(parts.path)

        try:
            urlretrieve(url, destination_name)
        except HTTPError as e:
            print(e)

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