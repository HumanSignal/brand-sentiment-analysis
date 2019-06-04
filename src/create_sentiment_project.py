"""
"""
import optparse
import heartex

CONFIG="""<View>
  <Text name="txt-1" value="$news"></Text>
  <Choices name="chc-1" toName="txt-1">
    <Choice value="Positive"></Choice>
    <Choice value="Netural"></Choice>
    <Choice value="Negative"></Choice>
    <Choice value="Other"></Choice>
  </Choices>
</View>"""


if __name__=="__main__":
    """
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-t', '--token', action="store", dest="token", help="heartex token")
    parser.add_option('-i', '--input', action="store", dest="input", default="filtered.csv", help="input file name")
    
    options, args = parser.parse_args()
    project = heartex.new_project_setup(**vars(options), label_config=CONFIG, name="Brand Sentiment Project")
    
    print("Visit this link and label:")
    print("https://go.heartex.net/expert/projects/%d/editor/" % (project, ))
