#!/bin/sh
#Script to run spider and store output in specific .json files
scrapy crawl nature_jobs_spider.py -o nature_jobs.json
scrapy crawl science_jobs_spider.py -o science_jobs.json
