"""
"""
import optparse
import csv

from GoogleNews import GoogleNews


def get_news(query=None, pages=1, *args, **kwargs):
    """
    """
    if query is None:
        raise Exception()
    
    news = []
    
    googlenews = GoogleNews()                                                                                              
    googlenews.search(query)
    
    for p in range(1, pages + 1):
        print(p)
        googlenews.getpage(p)
        news = news + googlenews.gettext()
    
    return news


if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-q', '--query', action="store", dest="query", help="query string")
    parser.add_option('-p', '--pages', action="store", type=int, dest="pages", default=10, help="number of pages to grab")
    parser.add_option('-o', '--output', action="store", dest="output", default="news.csv", help="csv output filename")
    
    options, args = parser.parse_args()    
    news = get_news(**vars(options))
    
    with open(options.output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames = ["news"])
        writer.writeheader()

        for row in news:
            writer.writerow({ "news": row })
