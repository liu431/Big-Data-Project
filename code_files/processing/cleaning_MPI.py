from mpi4py import MPI
import csv
import xml.sax
from bs4 import BeautifulSoup
import sys
import subprocess
import math


def xml_to_csv(file_name, max_lines=0):
    print('calling xml_to_csv')
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

    prefix = file_name
    if "." in prefix:
        prefix = prefix.split(".")[0]
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

    return [open(output_name, 'r+')]


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
        if col_names:
            self.attrs = col_names
        else:
            self.attrs = []
        self.out = output_name

    # Call when an element starts
    def startElement(self, tag, attributes):
        #print('calling startElement')
        self.current_data = tag
        if tag == "row":
            if not self.limit_lines:
                self.m_lines += 1
            if self.row < self.m_lines:
                self.row += 1
                if self.row == 1:
                    if not self.attrs:
                        self.attrs = list(attributes.keys())
                    write_row_to_csv(self.attrs, self.out)
                if len(attributes) > 0:
                    row_to_write = []
                    for a in self.attrs:
                        if a == 'AboutMe':
                            if a in attributes:
                                soup = BeautifulSoup(attributes[a], 'lxml')
                                text = soup.get_text()
                                if not text:
                                    text = ''
                                row_to_write.append(text)
                            else:
                                row_to_write.append('')
                        elif a == 'Body':
                            if a in attributes:
                                soup = BeautifulSoup(attributes[a], 'lxml')
                                all_p = soup.find_all('p')
                                processed_text = []
                                for tag in all_p:
                                    text = tag.get_text()
                                    processed_text.append(text)
                                processed_text = ' '.join(processed_text)
                                row_to_write.append(processed_text)
                        else:
                            val = attributes.get(a, '')
                            row_to_write.append(val)
                    write_row_to_csv(row_to_write, self.out)
        #print('done with row', self.row)


# executes a bash command, because sometimes Python is slow/bad at simple things
def exec_bash_cmd(cmd_str):
    print("Executing bash command: '" + cmd_str + "'")
    process = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error


def get_split_name(f_name, index):
    if index < 10:
        return f_name + "0" + str(index)
    return f_name + index

def fix_split_file(file_pre, j, max):
    if j != 0:
        # !!! ALTER THIS TO NOT BE HARDCODED, root parent is different from <tags> in different files
        exec_bash_cmd("sed -i '1s/^/<tags>\\n/' " + get_split_name(file_pre, j))
        exec_bash_cmd("sed -i '1s/^/<?xml version=\"1.0\" encoding=\"utf-8\"?>\\n/' " + get_split_name(file_pre, j))
    if j != max - 1:
        exec_bash_cmd('echo "</tags>" >> ' + get_split_name(file_pre, j))


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    name = MPI.Get_processor_name()

    if rank == 0:
        file_name = sys.argv[1]
        file_length = int(exec_bash_cmd("wc -l " + file_name + " | awk '{ print $1 }'")[0])
        # calc number of lines for each MP node
        file_prefix = file_name.split(".")[0]
        num_lines = math.ceil(file_length / size)
        print("Each node will process " + str(num_lines) + " lines")

        # split files using bash commands
        print(exec_bash_cmd("split -d -l " + str(num_lines) + " " + file_name + " " + file_prefix))

        # specify file chunks for each node to process
        for i in range(1, size):
            fix_split_file(file_prefix, i, size)
            comm.send(file_name, dest=i, tag=1)
            comm.send(num_lines, dest=i, tag=2)
            comm.send(file_prefix, dest=i, tag=3)
            comm.send(get_split_name(file_prefix, i), dest=i, tag=4)

        fix_split_file(file_prefix, 0, size)
        result = xml_to_csv(get_split_name(file_prefix, 0))
    else:
        file_name = comm.recv(source=0, tag=1)
        num_lines = comm.recv(source=0, tag=2)
        file_prefix = comm.recv(source=0, tag=3)
        processing_file_name = comm.recv(source=0, tag=4)
        try:
            file = open(processing_file_name, 'r')
        except FileNotFoundError:
            # split files using bash commands
            print(exec_bash_cmd("split -d -l " + str(num_lines) + " " + file_name + " " + file_prefix))
            for i in range(1, size):
                fix_split_file(file_prefix, i, size)
        result = xml_to_csv(processing_file_name)
