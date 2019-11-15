# coding=utf-8
import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils.misc import *

from config import journal_of_portfolio_folder

import traceback

from json import loads

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}


def fetch_issue(issue):
    r = requests.get(issue.url, headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')

    boxs = soup.find_all(
        attrs={
            'class': r'js-article-list-item'})
    articles = []
    for box in boxs:
        title = box.find(attrs={'class': r'js-article-title'})
        author = box.find(attrs={'class': r'js-article__item__authors'})
        url = r'https://www.sciencedirect.com/'+box.find(attrs={'class': r'article-content-title'})['href']
        r = requests.get(url,headers = headers,timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        doi = soup.find(attrs={'class': r'doi'})['href']
        abstract = soup.find(attrs={'id': r'aep-abstract-sec-id9'})
        article = Article(title=title.text if title else 'none',
                          author=author.text if author else 'none',
                          time=issue.coverDateText,
                          journal=issue.srctitle,
                          volume=issue.volumeFirst,
                          issue=issue.issueFirst,
                          url=url,
                          doi=doi)
        if abstract:
            article.set_abstract(abstract.text, text_abstract=True)
        articles.append(article)

        pass
    return


def fetch_all_links():
    root = r'https://www.sciencedirect.com/journal/journal-of-empirical-finance'
    issues = pd.DataFrame()
    from tqdm import trange
    for year in trange(1993,2020):
        r = requests.get(r'https://www.sciencedirect.com/journal/09275398/year/{}/issues'.format(year), headers=headers, timeout=15)
        issues = issues.append(loads(r.text)['data'],ignore_index=True)
    issues = issues.assign(root=root)
    issues = issues.assign(url=issues.root.str.cat(issues.uriLookup))
    issues.to_csv(r'',index=False)


def main():
    issues = fetch_all_links()
    fetch_issue(issues.iloc[0])
    return

if __name__ == '__main__':
    main()