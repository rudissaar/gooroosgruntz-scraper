#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class GooroogruntzScraper:
    _tasks = list()

    def __init__(self):
        print('__init__')

    def add_task(self, task):
        print(task)
        self._tasks.append(task)

    def run(self):
        print('run')

        if not self._tasks:
            self._tasks = ['battlez', 'questz']

        print(self._tasks)

