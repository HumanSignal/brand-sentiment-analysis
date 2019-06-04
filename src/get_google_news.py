"""
"""
import optparse
import requests
import html2text
import re
import pandas as pd

from datetime import datetime, timedelta
from urllib.parse import quote
from dateutil.parser import parse
from GoogleNews import GoogleNews
from readability import Document


def parse_date(date):
    m = re.match(r'^(\d+)\sminutes?\sago$', date)
    h = re.match(r'^(\d+)\shours?\sago$', date)
    if m:
        return int((datetime.now() - timedelta(minutes=int(m.group(1)))).timestamp())
    if h:
        return int((datetime.now() - timedelta(hours=int(h.group(1)))).timestamp())
    else:
        return int(parse(date).timestamp())


def get_news(query=None, pages=1, *args, **kwargs):
    """
    """
    if query is None:
        raise Exception()

    print(f'Start seaching query "{query}"')
    googlenews = GoogleNews()                                                                                              
    googlenews.search(quote(query))

    news = []
    seen_texts = set()
    for p in range(1, pages + 1):
        print(p)
        googlenews.getpage(p)
        r = googlenews.result()
        for item in r:
            try:
                timestamp = parse_date(item['date'])
                link = item['link']
                h = html2text.HTML2Text()
                h.ignore_links = True
                f = requests.get(link)
                html = f.text
                doc = Document(html)
                text = h.handle(doc.summary())
                if text not in seen_texts:
                    seen_texts.add(text)
                    text = re.sub(r'[\n\t]+', ' ', text)
                    news.append({'timestamp': timestamp, 'text': text})
            except Exception as exc:
                print(f'Exception while processing item {item}: {exc}')

    return news


if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-q', '--query', action="store", dest="query", help="query string")
    parser.add_option('-p', '--pages', action="store", type=int, dest="pages", default=10, help="number of pages to grab")
    parser.add_option('-o', '--output', action="store", dest="output", default="news.csv", help="output CSV file")
    
    options, args = parser.parse_args()    
    news = get_news(**vars(options))

    pd.DataFrame.from_records(news, columns=['timestamp', 'text']).sort_values(by='timestamp').to_csv(options.output, sep='\t', index=False)
    print(f'{len(news)} news are dumped to {options.output}.')
