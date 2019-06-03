"""
"""
import optparse
import json
import io
import requests
import html2text

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
                    news.append({'date': date, 'timestamp': timestamp, 'text': text})
                    seen_texts.add(text)

    return news


if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-q', '--query', action="store", dest="query", help="query string", default='Heartex')
    parser.add_option('-p', '--pages', action="store", type=int, dest="pages", default=10, help="number of pages to grab")
    parser.add_option('-o', '--output', action="store", dest="output", default="news.json", help="output JSON file")
    
    options, args = parser.parse_args()    
    news = get_news(**vars(options))
    
    with io.open(options.output, mode='w') as fout:
        json.dump(news, fout, indent=2, ensure_ascii=False)
    print(f'{len(news)} news are dumped to {options.output}.')
