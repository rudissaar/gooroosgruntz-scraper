#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line executable for GooroosgruntzScraper."""

import argparse

from gooroosgruntz_scraper import GooroosgruntzScraper

PARSER = argparse.ArgumentParser()

PARSER.add_argument('-b', '--battlez', help='scrape for battlez', action='store_true')
PARSER.add_argument('-q', '--questz', help='scrape for questz', action='store_true')
PARSER.add_argument('-v', '--verbose', help='make operations talkative', action='store_true')

ARGS = PARSER.parse_args()
VERBOSE = bool(ARGS.verbose)
SCRAPER = GooroosgruntzScraper(VERBOSE)

if ARGS.battlez:
    SCRAPER.add_task('battlez')
if ARGS.questz:
    SCRAPER.add_task('questz')

SCRAPER.run()
