#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from gooroogruntz_scraper import GooroogruntzScraper

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--battlez', help='crawl for battlez', action='store_true')
parser.add_argument('-q', '--questz', help='crawl for questz', action='store_true')
args = parser.parse_args()

scraper = GooroogruntzScraper()

if args.battlez:
    scraper.add_task('battlez')
if args.questz:
    scraper.add_task('questz')

scraper.run()

