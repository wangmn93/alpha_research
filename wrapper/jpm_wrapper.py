# coding=utf-8
import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils.misc import *

from config import journal_of_portfolio_folder

import traceback


def fetch_abstract(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find(attrs={'class': 'section abstract'}):
        abstract = soup.find(attrs={'class': 'section abstract'}).text.replace('Abstract', '')
        return abstract, True
    elif soup.find(attrs={'alt': 'PDF extract preview'}):
        img = soup.find(attrs={'alt': 'PDF extract preview'})['src']
        return img, False
    else:
        return 'no abstract', True


def fetch_issue(url):
    root = get_domain_name(url)
    r = requests.get(url,timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    boxs = soup.find_all(
        attrs={'class': 'highwire-cite highwire-cite-highwire-article highwire-citation-iij-list-complete clearfix'})
    articles = []
    for box in boxs:
        article = Article(title=box.find(attrs={'class': 'highwire-cite-linked-title'}).text,
                          author=box.find(attrs={'class': r'highwire-cite-authors'}).text,
                          doi=box.find(attrs={'class': 'highwire-cite-metadata-doi'}).text.replace('DOI: ', ''),
                          url=root + box.find(attrs={'class': 'highwire-cite-linked-title'})['href'],
                          time=box.find(attrs={'class': 'highwire-cite-metadata-coverdate'}).text,
                          journal=box.find(attrs={'class': 'highwire-cite-metadata-journal'}).text,
                          volume=box.find(attrs={'class': 'highwire-cite-metadata-volume'}).text,
                          issue=box.find(attrs={'class': 'highwire-cite-metadata-issue'}).text)
        abstract, is_text_abstract = fetch_abstract(article.url)
        article.set_abstract(abstract, is_text_abstract)
        articles.append(article)
    return articles


def fetch_all_links():
    urls = pd.read_csv(open(os.path.join(journal_of_portfolio_folder,'urls.csv')))
    url = str(urls.iloc[-1].urls)
    root = get_domain_name(url)
    get_next_page = lambda a: a.find(attrs={'rel': 'next'})
    try:
        from tqdm import tqdm
        with tqdm(total=1000) as pbar:
            while True:
                r = requests.get(url,timeout=15)
                soup = BeautifulSoup(r.text, 'html.parser')
                urls = urls.append({'urls':url},ignore_index=True)
                pbar.update()
                time.sleep(1)
                if get_next_page(soup):
                    url = root + get_next_page(soup)['href']
                else:
                    break
    except requests.Timeout as e:
        traceback.format_exc(e)
    finally:
        print('save urls')
        urls.drop_duplicates(subset='urls').to_csv(os.path.join(journal_of_portfolio_folder, 'urls.csv'),index=False)


def main():
    # fetch_volume(r'https://jpm.pm-research.com/content/36/4')
    fetch_all_links()

    return


if __name__ == '__main__':
    main()
