#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

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
