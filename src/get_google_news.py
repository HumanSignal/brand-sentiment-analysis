"""
"""
import optparse
import json
import io
import requests
import html2text
import re
import pandas as pd

from dateutil.parser import parse
from GoogleNews import GoogleNews
from readability import Document


def get_news(query=None, pages=1, *args, **kwargs):
    """
    """
    if query is None:
        raise Exception()
    
    googlenews = GoogleNews()                                                                                              
    googlenews.search(query)

    news = []
    seen_texts = set()
    for p in range(1, pages + 1):
        print(p)
        googlenews.getpage(p)
        r = googlenews.result()
        for item in r:
            try:
                date = item['date']
                timestamp = int(parse(date).timestamp())
            except:
                continue
            link = item['link']
            h = html2text.HTML2Text()
            h.ignore_links = True
            try:
                f = requests.get(link)
            except:
                continue
            else:
                html = f.text
                doc = Document(html)
                text = h.handle(doc.summary())
                if text not in seen_texts:
                    seen_texts.add(text)
                    text = re.sub(r'[\n\t]+', ' ', text)
                    news.append({'date': date, 'timestamp': timestamp, 'text': text})

    return news


if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-q', '--query', action="store", dest="query", help="query string", default='Heartex')
    parser.add_option('-p', '--pages', action="store", type=int, dest="pages", default=10, help="number of pages to grab")
    parser.add_option('-o', '--output', action="store", dest="output", default="news.csv", help="output TSV file")
    
    options, args = parser.parse_args()    
    news = get_news(**vars(options))

    pd.DataFrame.from_records(news).to_csv(options.output, sep='\t', index=False)
    print(f'{len(news)} news are dumped to {options.output}.')
