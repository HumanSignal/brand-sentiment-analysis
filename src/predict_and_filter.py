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
    parser.add_option('-i', '--input', action="store", dest="input", default="news.csv", help="input file name")
    
    options, args = parser.parse_args()

    data = []
    with open(options.input, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({ "text": row["news"] })

    predictions = heartex.run_predict(**vars(options), data=data)

    print(predictions)
