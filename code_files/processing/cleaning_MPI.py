from mpi4py import MPI
import csv
import xml.sax
from bs4 import BeautifulSoup
import sys
import subprocess
import math
import time


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
        # print('calling startElement')
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
        # print('done with row', self.row)


# executes a bash command, because sometimes Python is slow/bad at simple things
def exec_bash_cmd(cmd_str):
    print("Executing bash command: '" + cmd_str + "'")
    process = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error


def get_split_name(f_name, index):
    if index < 10:
        return f_name + "0" + str(index)
    return f_name + str(index)


def fix_split_file(file_pre, j, cluster_size):
    print("Fixing " + get_split_name(file_pre, j))
    if j != 0:
        exec_bash_cmd("sed -i '1s/^/<badges>\\n/' " + get_split_name(file_pre, j))
        exec_bash_cmd("sed -i '1s/^/<?xml version=\"1.0\" encoding=\"utf-8\"?>\\n/' " + get_split_name(file_pre, j))
    if j != cluster_size - 1:
        exec_bash_cmd('echo "</badges>" >> ' + get_split_name(file_pre, j))


def cleanup_files(file_pre, cluster_size):
    exec_bash_cmd("rm " + file_pre + "0*")
    if cluster_size > 9:
        exec_bash_cmd("rm " + file_pre + "1*")
    if cluster_size > 19:
        exec_bash_cmd("rm " + file_pre + "2*")


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    name = MPI.Get_processor_name()

    print("Starting node " + str(rank + 1) + " of " + str(size) + " on " + str(name))
    start = 0
    if rank == 0:
        num_hosts = 1
        file_name = sys.argv[1]
        if size > 1:
            file_length = int(exec_bash_cmd("wc -l " + file_name + " | awk '{ print $1 }'")[0])
            # calc number of lines for each MP node
            file_prefix = file_name.split(".")[0]
            num_lines = math.ceil(file_length / size)
            print("Each node will process " + str(num_lines) + " lines")

            cleanup_files(file_prefix, size)
            # split files using bash commands
            print(exec_bash_cmd("split -d -l " + str(num_lines) + " " + file_name + " " + file_prefix))

            # specify file chunks for each node to process
            # we don't need to send the actual file as it is expected to already be in the current directory
            for i in range(1, size):
                fix_split_file(file_prefix, i, size)
                comm.send(file_name, dest=i, tag=1)
                comm.send(num_lines, dest=i, tag=2)
                comm.send(file_prefix, dest=i, tag=3)
            fix_split_file(file_prefix, 0, size)  # XML files need a root element and header tag to be parsed correctly
            comm.barrier()
            # determine which nodes should split files, so files are only processed on each host once
            hostnames = name + ", " + str(comm.recv(source=(size - 1)))
            hostnames = hostnames.split(", ")
            print(hostnames)
            unique_hostnames = list(set(hostnames))
            num_hosts = len(unique_hostnames)
            host_prep = [True] * num_hosts
            for i in range(0, size):
                host_index = unique_hostnames.index(hostnames[i])
                if i != 0:
                    comm.send(int(host_prep[host_index]), dest=i, tag=5)
                if host_prep[host_index]:
                    print("Telling node " + str(i) + " to process file")
                    host_prep[host_index] = False
            comm.barrier()  # wait for all nodes to receive file process instructions
            comm.barrier()  # wait for all nodes to be ready to start
            start = time.time()  # start timing the conversion process
            print("Node " + str(rank) + " is processing " + get_split_name(file_prefix, rank))
            result = xml_to_csv(get_split_name(file_prefix, 0))  # convert the XML file to CSV
            comm.barrier()  # wait for all nodes to finish
        else:
            start = time.time()
            result = xml_to_csv(file_name)
        end = time.time()
        proc_time = end - start  # calculate processing time

        print("Processing with " + str(size) + " nodes on " + str(num_hosts) + " hosts took " + str(
            proc_time) + " seconds")
        # write results to csv with header
        try:
            file = open("results.csv", 'r')
        except FileNotFoundError:
            write_row_to_csv(["nodes", "hosts", "proc_time"], "results.csv")
        write_row_to_csv([size, num_hosts, proc_time], "results.csv")
    else:
        # get processing information from node 0
        file_name = comm.recv(source=0, tag=1)
        num_lines = comm.recv(source=0, tag=2)
        file_prefix = comm.recv(source=0, tag=3)
        comm.barrier()
        if rank == 1:
            if rank == size - 1:
                comm.send(str(name), dest=0)
            else:
                comm.send(str(name + ", "), dest=2)
        else:
            hostnames = str(comm.recv(source=(rank - 1))) + name
            if rank == size - 1:
                comm.send(hostnames, dest=0)
            else:
                hostnames = hostnames + ", "
                comm.send(hostnames, dest=(rank + 1))
        comm.barrier()
        split = bool(comm.recv(source=0, tag=5))
        # split files on other hosts
        if split:
            cleanup_files(file_prefix, size)
            # split files using bash commands
            print(exec_bash_cmd("split -d -l " + str(num_lines) + " " + file_name + " " + file_prefix))
            for i in range(0, size):
                fix_split_file(file_prefix, i, size)
        comm.barrier()  # wait for all nodes to be ready to start
        print("Node " + str(rank) + " is processing " + get_split_name(file_prefix, rank))
        result = xml_to_csv(get_split_name(file_prefix, rank))
        comm.barrier()  # wait for all nodes to finish
