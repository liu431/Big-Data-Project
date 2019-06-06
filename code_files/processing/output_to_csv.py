import sys
import csv
import time
from mpi4py import MPI
import numpy as np


def paste(*argv, sep=" "):
    out_string = ""
    for arg in argv:
        out_string = out_string + str(arg) + sep
    return out_string


def write_row_to_csv(row, out_filename):
    with open(out_filename, 'a', newline='') as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow(row)


def flatten_list(multid_list):
    out_list = []
    for item in multid_list:
        if isinstance(item, list):
            temp_list = flatten_list(item)
            for sub_item in temp_list:
                out_list.append(sub_item)
        else:
            out_list.append(item)
    return out_list


def process_line(in_line, strips, split):
    for char in strips:
        in_line = in_line.replace(char, "")
    in_line = in_line.replace("\t", " ")
    in_line = in_line.replace("\n", "")
    in_line = in_line.replace("\"", "")
    in_line = in_line.split(split)
    return in_line


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    name = MPI.Get_processor_name()

    print("Starting node " + str(rank + 1) + " of " + str(size) + " on " + str(name))

    args = iter(sys.argv)
    next(args)
    file_name = next(args)
    out_file_name = file_name.split(".")[0] + ".csv"
    split_char = next(args)
    if split_char == "space":
        split_char = " "
    strip_chars = []
    for s in args:
        strip_chars.append(s)

    out_lines = []
    num_lines = 0
    start = time.time()

    if rank == 0:
        print("Converting " + file_name + "; splitting on \'" + split_char, "\'; stripping " + str(strip_chars)[1:-1])
        file = open(file_name, "r")
        node = 0
        for line in file:
            if node == 0:
                out_lines.append(process_line(line, strip_chars, split_char))
                num_lines = num_lines + 1
            else:
                comm.send(line, dest=node)
            if node == size - 1:
                node = 0
            else:
                node = node + 1
        for node in range(1, size):
            comm.send("stop_running_file_now", dest=node)
            num_lines = num_lines + int(comm.recv(source=node))
    else:
        line = ""
        while line != "stop_running_file_now":
            if len(line) > 0:
                out_lines.append(process_line(line, strip_chars, split_char))
                num_lines = num_lines + 1
            line = comm.recv(source=0)
        comm.send(num_lines, dest=0)

    gathered_chunks = comm.gather(out_lines, root=0)

    if rank == 0:
        for chunk in gathered_chunks:
            for line in chunk:
                write_row_to_csv(line, out_file_name)
        end = time.time()
        proc_time = end - start
        print(paste("Processed", num_lines, "lines in", round(proc_time, 2), "seconds at an average",
                    round(num_lines / proc_time), "lines/sec"))
