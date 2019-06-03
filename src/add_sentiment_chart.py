# python3 script
import csv
import json
import optparse
import pandas as pd
import heartex
import time


def resample_by_time(times, values, period):
    """ Resample values by time

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


def run(options):
    """ 1 Read CSV with news
        2 Recognize sentiment using Haertex
        3 Collect positives and negatives
        4 Resample
        5 Save output json for chart
    """
    # read csv
    data = []
    with open(options.input, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            data.append({'text': row['text'], 'time': int(row['timestamp'])})

    # heartex predict
    predictions = heartex.run_predict(**vars(options), data=data)

    # collect score values (positives & negatives)
    for i, p in enumerate(predictions.json()):
        data[i]['value'] = 0
        if p['score'] > options.score:
            for row in p['result']:
                if 'Positive' in row['value']['choices']:
                    data[i]['value'] = +1
                if 'Negative' in row['value']['choices']:
                    data[i]['value'] = -1

    # resample
    times = [d['time'] for d in data]
    values = [d['value'] for d in data]
    x, y = resample_by_time(times, values, options.period)

    # save output
    output = {'data': data, 'chart': {'x': x, 'y': y}}
    with open(options.output, 'w') as f:
        json.dump(output, f)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    
    parser.add_option('-t', '--token', dest='token', help='heartex token')
    parser.add_option('-p', '--project', type=int, dest='project', help='project id')
    parser.add_option('-i', '--input', dest='input', default='news.csv', help='input file name')
    parser.add_option('-s', '--score', type=float, dest='score', default=0.50, help='score used to filter')
    parser.add_option('-d', '--period', dest='period', default='1D', help='pandas period: 1T (minute), 1H, 1D, 1M, 1Y')
    parser.add_option('-o', '--output', dest='output', default='output.json', help='output filename for charts')
    parser.add_option('-l', '--loop', action='store_true', dest='loop', default=False, help='run in loop')
    
    options, args = parser.parse_args()

    # rebuild news charts every 5 seconds
    while True:
        print(f'Run {options.input} => {options.output}')
        run(options)
        if not options.loop:
            break
        time.sleep(5)
