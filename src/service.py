#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import flask
import json  # it MUST be included after flask!
import heartex
import requests
import pandas as pd

from datetime import datetime as datetime
from flask import request
from utils import exception_treatment, answer, log_config, log


# init
config_path = sys.argv[1] if len(sys.argv) == 2 else 'config.json'
c = json.load(open(config_path))
app = flask.Flask(__name__, static_url_path='')
app.secret_key = 'A0Zr98jFFAQWjmdDWDQwfN]dddd/,?RfffdT'

# heartex
token = c['heartex']['token']
sentiment_project_id = c['heartex']['sentiment_project_id']


@app.route('/<path:path>')
def send_static(path):
    """ Static serving
    """
    return flask.send_from_directory('static', path)


@app.route('/logs')
def send_log():
    """ Log access via web
    """
    logfile = log_config['handlers']['file']['filename']
    return flask.send_file(open(logfile), mimetype='text/plain', as_attachment=False)


@app.route('/')
def index():
    """ Index.html, we don't use render template because it uses Vue for content render
    """
    return flask.send_from_directory('templates', 'index.html')


def get_tweets_from_database(query, start_date):
    """ Insert here request to your DB
    """
    '''return [
            {'text': 'cat runs', 'replies': ['bad', 'bad'], 'created_at': 123},
            {'text': 'dog stops', 'replies': ['awesome', 'super'], 'created_at': 567}
        ]'''

    if query == 'model:"Apple Watch"':
        query = 'Apple Watch'

    result = requests.get('http://tweets.makseq.com/api/tweets', params={'query': query, 'start_date': start_date})
    if result.status_code == 200:
        tweets = json.loads(result.content)
        return tweets
    else:
        raise Exception('Tweets DB error')


def resampling_by_time(times, values, period):
    """ Resampling values by time

    :param times: timestamps
    :param values: +1 and -1 or other float values
    :param period: 1T (minute), 1H, 1D, 1M, 1Y
    :return: x - time axis, y - values
    """
    data = pd.DataFrame({'time': pd.to_datetime(times, unit='s'), 'values': values})
    data = data.set_index('time').astype('float').resample(period)
    data = data.mean()

    data = data.fillna(0)
    x = data.index.astype(str).tolist()
    y = data.values[:, 0].tolist()

    return x, y


def heartex_build_plot(data, threshold_score=0.5, period='1D'):
    """ 1 Read data
        2 Recognize sentiment using Heartex
        3 Collect positives and negatives
        4 Resampling by time (to have one point per day)
        5 Format output json for chart

        :param data: tweets with replies
        :param threshold_score: use only replies with score is greater threshold, from 0.0 to 1.0
        :param period: resampling period (pandas style)
    """
    # pack tasks for Heartex prediction
    request_data = []
    for tweet in data:
        for reply in tweet['replies']:
            request_data.append({'text': reply})

    # heartex predict
    predictions = heartex.api.run_predict(token=token, project=sentiment_project_id, data=request_data).json()
    if not isinstance(predictions, list):
        raise Exception('Predictions are incorrect: ' + str(predictions))

    # unpack tasks back
    count = 0
    for tweet in data:
        tweet['predictions'] = []
        for _ in tweet['replies']:
            tweet['predictions'].append(predictions[count])
            count += 1

    # collect score values (positives & negatives)
    for tweet in data:
        total = 0
        tweet['sentiment'] = 0
        tweet['positives'] = 0
        tweet['negatives'] = 0

        # walk by predictions
        for prediction in tweet['predictions']:
            if prediction['score'] > threshold_score:

                if 'Positive' in prediction['result'][0]['value']['choices']:
                    total += 1
                    tweet['sentiment'] += 1
                    tweet['positives'] += 1

                elif 'Negative' in prediction['result'][0]['value']['choices']:
                    total += 1
                    tweet['sentiment'] -= 1
                    tweet['negatives'] -= 1

                # neutral
                else:
                    pass

        # normalize
        if total > 2:
            tweet['sentiment'] /= float(total)
        else:
            tweet['sentiment'] = 0  # disregard if there are too few replies

    # resampling sentiment
    times = [d['created_at'] for d in data]
    sentiment = [d['sentiment'] for d in data]
    sentiment_x, sentiment_y = resampling_by_time(times, sentiment, period)

    # resampling positives
    positives = [d['positives'] for d in data]
    positives_x, positives_y = resampling_by_time(times, positives, period)

    # resampling negatives
    negatives = [d['negatives'] for d in data]
    negatives_x, negatives_y = resampling_by_time(times, negatives, period)

    return {'news': data,
            'chart_sentiment': {'x': sentiment_x, 'y': sentiment_y},
            'chart_positives': {'x': positives_x, 'y': positives_y},
            'chart_negatives': {'x': negatives_x, 'y': negatives_y}}


@app.route('/api/build-sentiment', methods=['GET'])
@exception_treatment
def api_build_sentiment():
    """ Main service function: build sentiment analysis plot by query keyword.

    1. Get tweets and replies from database
    2. Send replies to Heartex predict to get sentiment scores
    3. Process predictions to plots

    :return: json with plot data
    """
    query = request.args['query']
    if len(query) < 2:
        return answer(422, 'small request', None)
    start_date = request.args['start_date']
    log.info('New query: %s' % str(request.args))

    tweets = get_tweets_from_database(query, start_date)
    log.info('Tweets found in DB %i' % len(tweets))

    output = heartex_build_plot(tweets)
    log.info('Heartex prediction completed')
    
    return answer(200, 'ok', output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=c['port'], debug=c['debug'])