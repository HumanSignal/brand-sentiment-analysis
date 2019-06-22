"""
"""
import optparse
import heartex

CONFIG="""<View>
  <Text name="txt-1" value="$news"></Text>
  <Labels name="chc-1" toName="txt-1">
%s
  </Labels>
</View>"""


if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-t', '--token', action="store", dest="token", help="heartex token")
    parser.add_option('-i', '--input', action="store", dest="input", default="news.csv", help="input file name")
    parser.add_option('-l', '--labels', type=str, dest="labels", action="store", help='A list of labels')
    
    options, args = parser.parse_args()

    labels = options.labels.split(',')
    
    labels_conf = "\n".join([ "    <Label value=\"%s\"></Label>" % (l,) for l in labels ])
    CONFIG = CONFIG % (labels_conf, )
    
    project = heartex.new_project_setup(**vars(options), label_config=CONFIG, name="Brand Filter Project")
    
    print("Visit this link and label:")
    print("https://go.heartex.net/expert/projects/%d/editor/" % (project, ))
