'''
Note
1. Users
2. Votes

row = '<row Id="1" Reputation="45742" CreationDate="2008-07-31T14:22:31.287" DisplayName="Jeff Atwood" LastAccessDate="2019-02-28T21:39:23.707" WebsiteUrl="http://www.codinghorror.com/blog/" Location="El Cerrito, CA" AboutMe="&lt;p&gt;&lt;a href=&quot;http://www.codinghorror.com/blog/archives/001169.html&quot; rel=&quot;nofollow&quot;&gt;Stack Overflow Valued Associate #00001&lt;/a&gt;&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Wondering how our software development process works? &lt;a href=&quot;http://www.youtube.com/watch?v=08xQLGWTSag&quot; rel=&quot;nofollow&quot;&gt;Take a look!&lt;/a&gt;&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Find me &lt;a href=&quot;http://twitter.com/codinghorror&quot; rel=&quot;nofollow&quot;&gt;on twitter&lt;/a&gt;, or &lt;a href=&quot;http://www.codinghorror.com/blog&quot; rel=&quot;nofollow&quot;&gt;read my blog&lt;/a&gt;. Don't say I didn't warn you &lt;em&gt;because I totally did&lt;/em&gt;.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;However, &lt;a href=&quot;http://www.codinghorror.com/blog/2012/02/farewell-stack-exchange.html&quot; rel=&quot;nofollow&quot;&gt;I no longer work at Stack Exchange, Inc&lt;/a&gt;. I'll miss you all. Well, &lt;em&gt;some&lt;/em&gt; of you, anyway. :)&lt;/p&gt;&#xA;" Views="454747" UpVotes="3373" DownVotes="1310" ProfileImageUrl="https://www.gravatar.com/avatar/51d623f33f8b83095db84ff35e15dbe8?s=128&amp;amp;d=identicon&amp;amp;r=PG" AccountId="1" />'

'''

import csv
from lxml import etree
from bs4 import BeautifulSoup



HEADERS = ['id', 'reputation', 'creationdate', 
            'displayname', 'lastaccessdate', 'websiteurl', 
            'location', 'aboutme', 'views', 
            'upvotes', 'downvotes', 'profileimageurl', 
            'accountid']

def write_row_to_csv(row):
    with open("sample_users.csv", "a", newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)


def process_single_line(line):
    soup = BeautifulSoup(line, "lxml")
    tag_attr_dict = soup.row.attrs
    rv = []
    for col in HEADERS:
        if col not in tag_attr_dict.keys():
            rv.append('')
        else:
            rv.append(tag_attr_dict[col])
    return rv


def process_xml_by_line(filepath):
    with open(filepath) as f:  
        line = f.readline() # skip row 0 
        line = f.readline() # skip row 1
        write_row_to_csv(HEADERS)
        for i in range(502):
            print("Line {}: {}".format(i, line.strip()))
            line = f.readline()
            line_list = process_single_line(line)
            write_row_to_csv(line_list)


if __name__ == '__main__':
    filepath = "./Users.xml"
    process_xml_by_line(filepath)

        