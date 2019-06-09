"""
CMSC 12300 / CAPP 30123
Task: Pre-processing data

Main author: Sanittawan (Nikki)
"""
import csv
from bs4 import BeautifulSoup
from lxml import etree


HEADERS_USERS = ['id', 'reputation', 'creationdate', 
                 'displayname', 'lastaccessdate', 'websiteurl', 
                 'location', 'aboutme', 'views', 
                 'upvotes', 'downvotes', 'profileimageurl', 
                 'accountid']

HEADERS_VOTES = ['id', 'postid', 'votetypeid', 'creationdate']

def write_row_to_csv(row, out_filename):
    """
    Write a single row to a CSV file in an appending mode

    Inputs:
        row: (list) of a single row
        out_filename: (string) name of the output file

    Returns: nothing
    """
    with open(out_filename, "a", newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)


def process_single_line(line, headers=None):
    """
    Clean a single line
    
    Inputs:
        line: (string) of a single line in XML file
        headers: (list) of the output CSV file

    Returns: (list) of a processed single line
    """
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
    """
    Read a single line from a file and process it

    Inputs:
        filepath: (string) path to the input file
        out_filename: (string) name of the output file
        headers: (list) of the headers of the output file

    Returns: nothing. Directly manipulate the output file
    """
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

