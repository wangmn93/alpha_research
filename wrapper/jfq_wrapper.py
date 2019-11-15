# coding=utf-8
import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils.misc import *

from config import journal_of_financial_and_quantitative_analysis

import traceback
import cfscrape

import subprocess

def fetch_issue(url):
    # result = subprocess.check_output(
    #     [r"node", "-v"], stdin=subprocess.PIPE, stderr=subprocess.PIPE,shell=True
    # )


    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    # Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session

    a = scraper.get(url)
    a.content
    # r = requests.get(url=url,headers=headers,timeout=15)

    return



def main():

    # with open(os.path.join(journal_of_financial_and_quantitative_analysis,r'issues.txt'),mode='r') as f:
    #     lines = f.readlines()
    #     urls = [r'https://www.cambridge.org'+ line.replace('\"','').replace('\n','').replace(' ','') for line in lines]
    #     pass
    fetch_issue(r'https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/issue/F6E479B2947E1ED69D5CB7F8FD479197')
    return

if __name__ == '__main__':
    main()