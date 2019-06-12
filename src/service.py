#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import flask
import json  # it MUST be included after flask!
import heartex

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
    return []


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


def heartex_build_plot(data, threshold_score, period):
    """ 1 Read data
        2 Recognize sentiment using Heartex
        3 Collect positives and negatives
        4 Resampling by time (to have one point per day)
        5 Save output json for chart
    """
    # pack tasks for Heartex prediction
    request_data = []
    for row in data:
        for reply in row['replies']:
            request_data.append({'text': reply})

    # heartex predict
    predictions = heartex.api.run_predict(token=token, project=sentiment_project_id, data=request_data)

    # unpack tasks back


    # collect score values (positives & negatives)
    for i, p in enumerate(predictions.json()):
        data[i]['value'] = 0
        if p['score'] > threshold_score:
            for row in p['result']:
                if 'Positive' in row['value']['choices']:
                    data[i]['value'] = +1
                if 'Negative' in row['value']['choices']:
                    data[i]['value'] = -1

    # resampling
    times = [d['time'] for d in data]
    values = [d['value'] for d in data]
    x, y = resampling_by_time(times, values, period)

    return {'news': data, 'chart': {'x': x, 'y': y}}


@app.route('/api/build-sentiment', methods=['GET'])
@exception_treatment
def api_build_sentiment():
    """ Main service function: build sentiment analysis plot by query keyword.
    1. Get tweets and replies from database
    2. Send replies to Heartex predict
    3. Process predictions to plots

    :return: json with plot data
    """
    query = request.args['query']
    start_date = request.args['start_date']
    tweets = get_tweets_from_database(query, start_date)




    log.info('New query: %s' % str(request.args))
    return answer(200, 'ok', {'test': 123})


if __name__ == "__main__":
    # to use audio recording we need https connection: ssl_context
    app.run(host='0.0.0.0', port=c['port'], debug=c['debug'])