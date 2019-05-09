import csv
from lxml import etree
from bs4 import BeautifulSoup


HEADERS_USERS = ['id', 'reputation', 'creationdate', 
                 'displayname', 'lastaccessdate', 'websiteurl', 
                 'location', 'aboutme', 'views', 
                 'upvotes', 'downvotes', 'profileimageurl', 
                 'accountid']

HEADERS_VOTES = ['id', 'postid', 'votetypeid', 'creationdate']

def write_row_to_csv(row, out_filename):
    with open(out_filename, "a", newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)


def process_single_line(line, headers=None):
    soup = BeautifulSoup(line, "lxml")
    tag_attr_dict = soup.row.attrs
    print(tag_attr_dict.keys())
    rv = []
    for col in headers:
        if col not in tag_attr_dict.keys():
            rv.append('')
        else:
            rv.append(tag_attr_dict[col])
    return rv


def process_xml_by_line(filepath, out_filename, headers=None):
    with open(filepath) as f:  
        line = f.readline() # skip row 0 
        line = f.readline() # skip row 1
        write_row_to_csv(headers, out_filename)
        for i in range(502):
            print("Line {}: {}".format(i, line.strip()))
            line = f.readline()
            line_list = process_single_line(line, headers)
            write_row_to_csv(line_list, out_filename)


if __name__ == '__main__':
    users_filepath = "./Users.xml"
    users_csv = "sample_users.csv"
    process_xml_by_line(users_filepath, users_csv, HEADERS_USERS)
    votes_filepath = "./Votes.xml"
    votes_csv = "sample_votes.csv"
    process_xml_by_line(votes_filepath, votes_csv, HEADERS_VOTES)

