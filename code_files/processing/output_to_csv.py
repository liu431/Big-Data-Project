"""
This script takes an output text file with string representations of lists and converts it to a CSV
Author: Adam Shelton
"""
import sys
import csv
import time
from mpi4py import MPI
import numpy as np
import ast


def paste(*argv, sep=" "):
    """
    Pastes the string representation of arguments together, separating them by a string
    :param argv: Unlimited arguments to convert to string and combine
    :param sep: A string that will separate other strings, by default is a space (' ')
    :return: A string containing the string representations of objects passed in as *argv, separated by sep;
            an equivalent of the paste function in R
    """
    out_string = ""
    for arg in argv:
        out_string = out_string + str(arg) + sep
    return out_string


def write_row_to_csv(row, out_filename):
    """
    Writes a row of a processed file to CSV
    :param row: A list of items to write to CSV, each item in a list becomes a column in row
    :param out_filename: A string giving the filename to write the CSV to
    """
    with open(out_filename, 'a', newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)


def flatten_list(multid_list):
    """
    Flattens a multi-dimensional list (list-ception) into a one-dimensional list, using recursion
    :param multid_list: A list to flatten
    :return: A one-dimensional flattened list
    """
    out_list = []
    for item in multid_list:
        if isinstance(item, list):
            temp_list = flatten_list(item)
            for sub_item in temp_list:
                out_list.append(sub_item)
        else:
            out_list.append(item)
    return out_list


def process_line(in_line):
    """
    Processes a line from the file to prepare it for writing to CSV
    :param in_line: A string containing a line from a file
    :return: A processed flatten list of strings
    """
    if "null" in in_line:
        in_line = in_line.replace("null", "\"NA\"")  # replace nulls with NA strings
    in_line = in_line.split("\t")  # split lines by any tabs
    for i in range(len(in_line)):
        in_line[i] = ast.literal_eval(in_line[i])  # convert string representation of object to that actual object
    return flatten_list(in_line)


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    name = MPI.Get_processor_name()

    args = iter(sys.argv)
    next(args)
    file_name = next(args)  # get name of file to process from script argument
    out_file_name = file_name.split(".")[0] + ".csv"  # create output CSV filename

    if rank == 0:  # some status messages
        print("Converting " + file_name)
    print("Starting node " + str(rank + 1) + " of " + str(size) + " on " + str(name))

    out_lines = []
    num_lines = 0
    start = time.time()  # start the timer

    if rank == 0:  # node 0 splits the file to distribute to other nodes
        print(paste("Splitting", file_name))
        with open(file_name) as file:
            all_lines = file.readlines()
        input_chunks = np.array_split(all_lines, size)
    else:
        input_chunks = None

    if rank == 0:  # node 0 scatters the split chunks to other nodes
        print(paste("Scattering", file_name))
    chunk = comm.scatter(input_chunks, root=0)

    if rank == 0:  # process some lines and count how many lines are processed
        paste("Processing chunks")
    for line in chunk:
        out_lines.append(process_line(line))
        num_lines = num_lines + 1
    comm.barrier()  # wait for all nodes to finish processing

    if rank == 0:  # all nodes send how many lines they processed to node 0 to find total lines processed
        for node in range(1, size):
            comm.send("go", dest=node)
            num_lines = num_lines + int(comm.recv(source=node))
        print("Gathering chunks")
    else:
        comm.recv(source=0)
        comm.send(num_lines, dest=0)
    comm.barrier()

    gathered_chunks = comm.gather(out_lines, root=0)  # gather split data chunks from each node on node 0

    if rank == 0:  # node 0 takes all processed lines and writes them to a CSV on that host
        print("Writing lines to CSV")
        for chunk in gathered_chunks:
            for line in chunk:
                write_row_to_csv(line, out_file_name)
        end = time.time()
        proc_time = end - start
        print(paste("Processed", num_lines, "lines in", round(proc_time, 2), "seconds at an average",
                    round(num_lines / proc_time), "lines/sec"))  # print some stats about the process
