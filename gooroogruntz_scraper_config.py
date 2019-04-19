#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

from shutil import copyfile

class GooroogruntzScraperConfig:
    def __init__(self):
        self._container = os.path.dirname(os.path.realpath(__file__))

        if not self._container.endswith('/'):
            self._container += '/'

        self._config_path = self._container + 'config.json'

        if not os.path.isfile(self._config_path):
            copyfile(self._container + 'config.json.sample', self._config_path)

        with open(self._config_path, 'r') as file_handle:
            data = json.load(file_handle)

        print(data)
