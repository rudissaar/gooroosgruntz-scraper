#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains GooroosgruntzScraperConfig class."""

import json
import os

from shutil import copyfile

class GooroosgruntzScraperConfig:
    """Class that reads in configuration from json file and provides extra functionalities."""

    _config = dict()

    def __init__(self):
        """Constructor of the GooroosgruntzScraperConfig class."""

        self._container = os.path.dirname(os.path.realpath(__file__))

        if not self._container.endswith('/'):
            self._container += '/'

        self._config_path = self._container + 'config.json'

        if not os.path.isfile(self._config_path):
            copyfile(self._container + 'config.json.sample', self._config_path)

        with open(self._config_path, 'r') as file_handle:
            data = json.load(file_handle)

        try:
            self._config['date_based_names'] = data['date_based_names']
        except KeyError:
            self._config['date_based_names'] = False

        try:
            self._config['battlez_urls'] = data['battlez']['urls']
        except KeyError:
            self._config['battlez_urls'] = None

        try:
            self._config['questz_urls'] = data['questz']['urls']
        except KeyError:
            self._config['questz_urls'] = None

    @property
    def date_based_names(self):
        """Getter for date_based_names property."""

        return self._config['date_based_names']

    @property
    def battlez_urls(self):
        """Getter for battlez_urls property."""

        return self._config['battlez_urls']

    @property
    def questz_urls(self):
        """Getter for questz_urls property."""

        return self._config['questz_urls']
