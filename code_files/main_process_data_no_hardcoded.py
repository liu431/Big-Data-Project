'''
votes_columns = [Id, PostId, VoteTypeId, UserId, CreationDate]

Posts_columns = [Id, PostTypeId, ParentId, AcceptedAnswerId, 
CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, 
LastEditorDisplayName, LastEditDate, LastActivityDate, 
Title, Tags, AnswerCount, CommentCount, FavoriteCount, 
CommunityOwnedDate, CommentCount]

"<p>Hi, I'm not really a person.</p>

<p>I'm a background process that helps keep this site clean!</p>

<p>I do things like</p>

<ul>
<li>Randomly poke old unanswered questions every hour so they get some attention</li>
<li>Own community questions and answers so nobody gets unnecessary reputation from them</li>
<li>Own downvotes on spam/evil posts that get permanently deleted</li>
<li>Own suggested edits from anonymous users</li>
<li><a href=""http://meta.stackexchange.com/a/92006"">Remove abandoned questions</a></li>
</ul>
"
'''

import csv
import xml.sax
import sys
from bs4 import BeautifulSoup

def xml_to_csv(file_name, max_lines=0):
    VOTES_COLS = ["Id", "PostId", "VoteTypeId", "UserId", "CreationDate"]

    POSTS_COLS = ["Id", "PostTypeId", "ParentId", "AcceptedAnswerId",
                  "CreationDate", "Score", "ViewCount", "Body", "OwnerUserId",
                  "LastEditorUserId", "LastEditorDisplayName", "LastEditDate",
                  "LastActivityDate", "Title", "Tags", "AnswerCount",
                  "FavoriteCount", "CommunityOwnedDate", "CommentCount",
                   "OwnerDisplayName", "DeletionDate", "ClosedDate"]

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    prefix = file_name.split(".")[0]
    output_name = prefix + ".csv"
    # override the default ContextHandler
    if prefix == 'Votes':
        col_names = VOTES_COLS
    elif prefix == 'Posts':
        col_names = POSTS_COLS
    else:
        col_names = None
    Handler = SOHandler(output_name, max_lines, col_names)
    parser.setContentHandler(Handler)
    parser.parse(file_name)


def write_row_to_csv(row, out_filename):
    with open(out_filename, 'a', newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)


class SOHandler(xml.sax.ContentHandler):
    def __init__(self, output_name, max_lines, col_names=None):
        self.current_data = ""
        self.row = 0
        self.limit_lines = max_lines != 0
        self.m_lines = max_lines
        if not col_names:
            self.attrs = col_names
        else:
            self.attrs = []
        self.out = output_name

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "row":
            if not self.limit_lines:
                self.m_lines += 1
            if self.row < self.m_lines:
                self.row += 1
                if self.row == 1:
                    self.attrs = list(attributes.keys())
                    write_row_to_csv(self.attrs, self.out)
                if len(attributes) > 0:
                    row_to_write = []
                    for a in self.attrs:
                        if a == 'AboutMe':
                            if a in attributes:
                                soup = BeautifulSoup(attributes[a], 'lxml')
                                about_me_text = soup.get_text()
                                row_to_write.append(about_me_text)
                        else:
                            val = attributes.get(a, '')
                            row_to_write.append(val)
                    write_row_to_csv(row_to_write, self.out)

if (__name__ == "__main__"):
    if len(sys.argv) == 2:
        xml_to_csv(sys.argv[1])
    if len(sys.argv) == 3:
        xml_to_csv(sys.argv[1], int(sys.argv[2]))


