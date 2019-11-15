from urllib.parse import *
from jinja2 import Environment, FileSystemLoader, select_autoescape


__all__ = ['headers','Article','get_domain_name']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}


env = Environment(
    loader=FileSystemLoader(searchpath=r'../templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class Article:
    def __init__(self, title, author, time, journal, volume, issue, url, doi):
        self.title = title
        self.authors = author,
        self.time = time
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.url = url
        self.scihub = r'https://sci-hub.tw/'+doi
        self.doi = doi
        self.abstract = 'no abstract'
        self.text_abstract = True

    def set_abstract(self, abstract, text_abstract):
        self.abstract = abstract
        self.text_abstract = text_abstract

    def __str__(self):
        return '{},{}, {} {} {} {} '.format(self.title ,self.authors, self.time, self.journal,self.volume,self.issue, )

    def get_dict(self):
        return dict(title=self.title,
                    journal=self.journal,
                    volume=self.volume,
                    issue=self.issue,
                    url=self.url,
                    doi=self.doi,
                    abstract=self.abstract)

    def render_html(self, template='article.html'):
        return env.get_template(template).render(article=self)


def get_domain_name(url):
    scheme, netloc, path, query, fragment = urlsplit(url)
    return scheme+'://'+netloc


def main():
    get_domain_name(r'https://jpm.pm-research.com/content/36/4')
    article = Article('a','b','c','d','e','f','g','h',False)
    html = article.render_html()
    return


if __name__ == '__main__':
    main()
