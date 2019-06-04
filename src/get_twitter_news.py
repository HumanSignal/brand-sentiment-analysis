"""
"""
import optparse
import twitter
import csv
import urllib


def get_news(query=None, channels=None, pages=1,
             consumer_key=None, consumer_secret=None,
             oauth_token=None,oauth_secret=None,
             *args, **kwargs):
    """
    """
    last_id   = None
    part_size = 10
    total     = 100
    tweets    = []
    
    api = twitter.Api(consumer_key, consumer_secret, oauth_token, oauth_secret)
    
    # we can request maximum 200 tweets per request
    for i in range(0, total, part_size): 
        try:
            result = api.GetSearch(term=query, count=part_size, since_id=last_id)  
        except twitter.error.TwitterError as e:
            print('\n\n-- Twitter rate exceeded (or another error) --')
            print(e)
            return tweets	
        if result:
            # convert twitter objects to dicts
            tweets = tweets + [ r.AsDict() for r in result ] 
            target = result[-1].id
            
            if last_id == target:
                break
            
            last_id = target
        else: # result is empty
            break
    
    return tweets

if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-q', '--query', action="store", dest="query", help="query string")
    parser.add_option('-p', '--pages', action="store", type=int, dest="pages", default=10, help="number of pages to grab")
    parser.add_option('-o', '--output', action="store", dest="output", default="news.csv", help="csv output filename")

    parser.add_option('--consumer-key', action="store", dest="consumer_key", help="Twitter consumer key")
    parser.add_option('--consumer-secret', action="store", dest="consumer_secret", help="Twitter consumer secret")
    parser.add_option('--oauth-token', action="store", dest="oauth_token", help="Twitter oauth token")
    parser.add_option('--oauth-secret', action="store", dest="oauth_secret", help="Twitter oauth secret")    
    
    options, args = parser.parse_args()    
    news = get_news(**vars(options))
    fieldnames = ['created_at', 'news', 'username']
    
    with open(options.output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        
        for row in news:
            data = {
                "news": row['text'],
                "created_at": row['created_at'],
                "username": row['user']['screen_name']
            }
            
            writer.writerow(data)
