import pdfkit
import os
from config import wkhtmltopdf
__all__ = ['save_to_pdf','save_to_html']
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
dir()
def save_to_pdf(htmls, names, folder):
    if len(names)==1:
        pdfkit.from_file(htmls, os.path.join(folder, '{}.pdf'.format(names[0])), configuration=config,
                         options={'encoding': "UTF-8"})
        return
    if len(htmls) == len(names):
        for name, html in zip(names, htmls):
            pdfkit.from_file(htmls, os.path.join(folder, '{}.pdf'.format(name)), configuration=config,
                             options={'encoding': "UTF-8"})
        return
    raise ValueError('文件数量和名字数量不匹配')

    return

def save_to_html(htmls, names, folder):
    return
def save_pdf(url):
    print(url)
    articles = find_articles(url)
    volume, issue = articles[0]['volume'], articles[0]['issue']
    folder = r'C:\Users\Administrator\Desktop\因子文献\jpm_title\{}_{}'.format(volume, issue).replace(' ', '')
    if not os.path.exists(folder):
        os.mkdir(folder)
    pd.DataFrame(articles).to_csv(os.path.join(folder, 'content.csv'), index=False)
    htmls = []
    template = '<html><h1>{0} <a href="https://sci-hub.tw/{7}">[sci-hub]</a></h1>{1},date {2},volume {3},issue {4},page{5}<p></p><a href="{6}">{6}</a><p/><a href="{7}">doi: {7}</a>{8}</html>'
    for article in tqdm(articles):
        abstract = find_abs(article['href'])
        if abstract.endswith('.jpg'):
            abstract = r'<img src="{}" alt="abstract">'.format(abstract)
        else:
            abstract = r'<p>{}</p>'.format(abstract)
        html = template.format(article['title'], article['journal'], article['date'], article['volume'],
                               article['issue'], article['page'], article['href'], article['doi'], abstract)
        #         print(html)
        filename = r'{}{}{}.html'.format(article['volume'], article['issue'], article['page'])
        with open(os.path.join(folder, filename), 'w', encoding='utf8') as f:
            f.write(html)
        htmls.append(os.path.join(folder, filename))
    pdfkit.from_file(htmls, os.path.join(folder, 'content.pdf'), configuration=config,
                     options={'encoding': "UTF-8"})