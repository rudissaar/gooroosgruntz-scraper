#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Scraper designed to scrape custom Gruntz levels from http://gooroosgruntz.proboards.com"""

import os
import re
import shutil
import zipfile

from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from gooroosgruntz_scraper_config import GooroosgruntzScraperConfig

class GooroosgruntzScraper:
    """Main class that performs scraping process."""

    _tasks = list()
    _pages = list()
    _urls = list()

    def __init__(self, verbose=False, debug=False):
        self._verbose = verbose
        self._debug = debug

        self._container = os.path.dirname(os.path.realpath(__file__))
        self._config = GooroosgruntzScraperConfig()

        if os.path.exists(self._container + '/tmp'):
            shutil.rmtree(self._container + '/tmp')

        os.mkdir(self._container + '/tmp', 0o700)

        if not os.path.exists(self._container + '/loot'):
            os.mkdir(self._container + '/loot', 0o700)

    def add_task(self, task):
        """Method that adds tasks to scrape, also checks for duplications."""

        if task not in self._tasks:
            self._tasks.append(task)

    def process_task(self, task):
        """Method that handles flushing buffers and triggering subtasks."""

        self._pages.clear()
        self._urls.clear()

        self.paginate(task)
        self.spider()
        self.scrape(task)
        self.package(task)

    def run(self):
        """Method that actually starts the flow."""

        if not self._tasks:
            self.add_task('battlez')
            self.add_task('questz')

        for task in self._tasks:
            self.process_task(task)

    def paginate(self, task, page=None):
        """Method that collects pages to scraped later."""

        if page is None:
            page = getattr(self._config, task + '_urls').pop(0)

        self._pages.append(page)

        soup = self.get_soup(page, self._debug)
        pagination = soup.find('ul', {'class': ['ui-pagination']})
        next_page = pagination.findChild('li', {'class': 'next'})

        if next_page:
            link = next_page.findChild('a', href=True)

            if link:
                self.paginate(task, self.get_domain(page) + link['href'])
            elif not link and getattr(self._config, task + '_urls'):
                self.paginate(task)

    def spider(self):
        """Method that collects urls of individual levels."""

        for page in self._pages:
            soup = self.get_soup(page, self._debug)
            domain = self.get_domain(page)
            elements = soup.findAll('tr', {'class': ['item', 'thread']})

            for element in elements:
                if 'announcement' in element['class']:
                    continue

                link = element.findChild('a', {'class': 'thread-link'})
                self._urls.append(domain + link['href'])

    def scrape(self, task):
        """Method that searches for download links and pulls them down."""

        for url in self._urls:
            soup = self.get_soup(url, self._debug)
            buttons = soup.findAll('img', {'src': re.compile('Download.gif$', re.I)})

            for button in buttons:
                if button.parent.name == 'a':
                    link = button.parent['href']
                    pattern = re.compile('.wwd$', re.I)

                    if pattern.search(urlparse(link).path):
                        self.download_file(task, link)

    def package(self, task):
        """Method that creates archive from levels that just got pulled down."""

        zip_path = self._container + '/loot/gruntz-' + task + '.zip'
        amount = 0

        zip_handle = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

        for root, _, files in os.walk(self._container + '/tmp/' + task):
            for file in files:
                zip_handle.write(os.path.join(root, file), file)
                amount += 1

        if amount:
            new_zip_path = self._container + '/loot/gruntz-' + task + '-' + str(amount) + '.zip'
            os.rename(zip_path, new_zip_path)
        else:
            os.remove(zip_path)

    def download_file(self, task, url):
        """Method that downloads file from specified url."""

        destination_dir = self._container + '/tmp/' + task

        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir, 0o700)

        parts = urlparse(url)
        destination_name = destination_dir + '/' + os.path.basename(parts.path)

        try:
            urlretrieve(url, destination_name)
        except HTTPError:
            pass

    @staticmethod
    def get_domain(url):
        """Static method that return domain with scheme from specified url."""

        parts = urlparse(url)
        return parts.scheme + '://' + parts.netloc

    @staticmethod
    def get_soup(url, debug=False):
        """Static method that parses specified url and returns soup handle if possible."""

        try:
            if debug:
                print('> Getting soup from: ' + url)
            html = urlopen(url)
            soup = BeautifulSoup(html.read(), 'html.parser')
        except HTTPError as exception:
            if debug:
                print('> Getting soup failed: ' + exception.reason)
            return None
        except URLError as exception:
            if debug:
                print('> Getting soup failed: ' + exception.reason)
            return None
        else:
            return soup
