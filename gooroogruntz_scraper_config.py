#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

from shutil import copyfile

class GooroogruntzScraperConfig:
    _config = dict()

    def __init__(self):
        self._container = os.path.dirname(os.path.realpath(__file__))

        if not self._container.endswith('/'):
            self._container += '/'

        self._config_path = self._container + 'config.json'

        if not os.path.isfile(self._config_path):
            copyfile(self._container + 'config.json.sample', self._config_path)

        with open(self._config_path, 'r') as file_handle:
            data = json.load(file_handle)

        try:
            self._config['battlez_urls'] = data['battlez']['urls']
        except KeyError:
            self._config['battlez_urls'] = None

        try:
            self._config['questz_urls'] = data['questz']['urls']
        except KeyError:
            self._config['questz_urls'] = None

    @property
    def battlez_urls(self):
        return self._config['battlez_urls']

    @property
    def questz_urls(self):
        return self._config['questz_urls']
