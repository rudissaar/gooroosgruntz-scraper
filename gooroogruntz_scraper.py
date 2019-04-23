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

    def __init__(self):
        self._container = os.path.dirname(os.path.realpath(__file__))
        self._config = GooroogruntzScraperConfig()

    def add_task(self, task):
        self._tasks.append(task)

    def run(self):
        if not self._tasks:
            self._tasks = ['battlez', 'questz']

        if 'battlez' in self._tasks:
            self.scrape_battlez()

        if 'questz' in self._tasks:
            self.scrape_questz()

    def scrape_battlez(self):
        urls = list()        

        try:
            html = urlopen(self._config.battlez_url)
            soup = BeautifulSoup(html.read(), 'html.parser')
        except HTTPError as err:
            print(err)
            return
        except URLError as err:
            print(err)
            return

        urls.append(self._config.battlez_url)

        pagination = soup.find('ul', {'class': ['ui-pagination']})
        pages = pagination.findChildren('li')

        for page in pages:
            try:
                if 'next' in page['class']:
                    link = page.findChild('a', href=True)

                    if link:
                        print(link['href'])
            except KeyError:
                continue

    def scrape_questz(self):
        print(self._config.questz_url)
