'''
votes_columns = [Id, PostId, VoteTypeId, UserId, CreationDate]

Posts_columns = [Id, PostTypeId, ParentId, AcceptedAnswerId, 
CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, 
LastEditorDisplayName, LastEditDate, LastActivityDate, 
Title, Tags, AnswerCount, CommentCount, FavoriteCount, 
CommunityOwnedDate, CommentCount]
'''

import csv
import xml.sax
import sys

def xml_to_csv(file_name, max_lines=0):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    output_name = file_name.split(".")[0] + ".csv"
    # override the default ContextHandler
    Handler = SOHandler(output_name, max_lines)
    parser.setContentHandler(Handler)
    parser.parse(file_name)

'''
Courtesy of Nikki
'''
def write_row_to_csv(row, out_filename):
    with open(out_filename, "a", newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)

class SOHandler(xml.sax.ContentHandler):
    def __init__(self, output_name, max_lines):
        self.CurrentData = ""
        self.row = 0
        self.limit_lines = max_lines != 0
        self.m_lines = max_lines
        self.out = output_name

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "row":
            if not self.limit_lines:
                self.m_lines = self.m_lines + 1
            if self.row < self.m_lines:
                self.row = self.row + 1
                if self.row == 1:
                    write_row_to_csv(attributes.keys()[1:-1], self.out)
                if len(attributes) > 0:
                    write_row_to_csv(attributes.values()[1:-1], self.out)

if (__name__ == "__main__"):
    if len(sys.argv) == 2:
        xml_to_csv(sys.argv[1])
    if len(sys.argv) == 3:
        xml_to_csv(sys.argv[1], int(sys.argv[2]))
