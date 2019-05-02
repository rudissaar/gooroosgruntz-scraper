#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

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

    def add_task(self, task):
        self._tasks.append(task)

    def run(self):
        if not self._tasks:
            self._tasks = ['battlez', 'questz']

        if 'battlez' in self._tasks:
            self.paginate_battlez()
            self.spider_battlez()
            print(len(self._urls))

        if 'questz' in self._tasks:
            self.scrape_questz()

    def paginate_battlez(self, page=None):
        if page is None:
            page = self._config.battlez_url

        try:
            html = urlopen(page)
            soup = BeautifulSoup(html.read(), 'html.parser')
        except HTTPError as err:
            print(err)
            return
        except URLError as err:
            print(err)
            return

        self._pages.append(page)

        pagination = soup.find('ul', {'class': ['ui-pagination']})
        next_page = pagination.findChild('li', {'class': 'next'})
        
        if next_page:
            link = next_page.findChild('a', href=True)

            if link:
                self.paginate_battlez(self.get_domain(self._config.battlez_url) + link['href'])

    def spider_battlez(self):
        for page in self._pages:
            try:
                html = urlopen(page)
                soup = BeautifulSoup(html.read(), 'html.parser')
            except HTTPError as err:
                print(err)
                return
            except URLError as err:
                print(err)
                return

            domain = self.get_domain(page)
            elements = soup.findAll('tr', {'class': ['item', 'thread']})

            for element in elements:
                if 'announcement' in element['class']:
                    continue

                link = element.findChild('a', {'class': 'thread-link'})
                self._urls.append(domain + link['href'])

    def scrape_questz(self):
        print(self._config.questz_urls)

    @staticmethod
    def get_domain(url):
        parts = urlparse(url)
        return (parts.scheme + '://'+ parts.netloc)
