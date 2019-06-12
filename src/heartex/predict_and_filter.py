"""
"""
import csv
import optparse
import heartex

if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-t', '--token', action="store", dest="token", help="heartex token")
    parser.add_option('-p', '--project', action="store", type=int, dest="project", help="project id")
    parser.add_option('-s', '--score', action="store", type=float, dest="score", default=0.90, help="score used to filter")
    parser.add_option('-i', '--input', action="store", dest="input", default="news.csv", help="input file name")
    parser.add_option('-o', '--output', action="store", dest="output", default="filtered.csv", help="csv output filename")
    parser.add_option('-l', '--filter-labels', type=str, dest="filter_labels", action="store", help='A list of labels to filter on')
    
    options, args = parser.parse_args()
    labels = options.filter_labels.split(',')
    
    data = []
    with open(options.input, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({ "news": row["news"] })
    
    predictions = heartex.run_predict(**vars(options), data=data)
    filtered = []
    
    for idx, p in enumerate(predictions.json()):
        if p['score'] > options.score:
            for row in p['result']:
                for label in labels:
                    if label in row['value']['labels']:
                        filtered.append(data[idx])
                        break
    
    with open(options.output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames = ["news"])
        writer.writeheader()
        
        for row in filtered:
            writer.writerow(row)
    
    print(len(predictions.json()))
    print(len(filtered))
