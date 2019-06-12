#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import flask
import json  # it MUST be included after flask!
import pandas as pd
import heartex

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
    return [
        {'text': 'cat runs', 'replies': ['bad', 'bad'], 'created_at': 'Thu May 23 18:03:00 +0000 2019'},
        {'text': 'dog stops', 'replies': ['awesome', 'super'], 'created_at': 'Fri Jun 07 13:45:00 +0000 2019'}
    ]


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
    print(predictions)

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
        tweet['value'] = 0

        for prediction in tweet['predictions']:
            if prediction['score'] > threshold_score:
                total += 1

                if 'Positive' in prediction['result'][0]['value']['choices']:
                    tweet['value'] += 1

                if 'Negative' in prediction['result'][0]['value']['choices']:
                    tweet['value'] -= 1

            # normalize
            tweet['value'] /= float(total)

    # resampling
    times = [datetime.strptime(d['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timestamp() for d in data]
    values = [d['value'] for d in data]
    x, y = resampling_by_time(times, values, period)

    return {'news': data, 'chart': {'x': x, 'y': y}}


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
    start_date = request.args['start_date']

    tweets = get_tweets_from_database(query, start_date)
    output = heartex_build_plot(tweets)

    log.info('New query: %s' % str(request.args))
    return answer(200, 'ok', output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=c['port'], debug=c['debug'])