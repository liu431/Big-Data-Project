import sys
import csv
import time
from mpi4py import MPI
import numpy as np
import ast


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


def process_line(in_line):
    if "null" in in_line:
        in_line = in_line.replace("null", "\"NA\"")
    in_line = in_line.split("\t")
    for i in range(len(in_line)):
        in_line[i] = ast.literal_eval(in_line[i])
    return flatten_list(in_line)


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    name = MPI.Get_processor_name()

    args = iter(sys.argv)
    next(args)
    file_name = next(args)
    out_file_name = file_name.split(".")[0] + ".csv"

    if rank == 0:
        print("Converting " + file_name)
    print("Starting node " + str(rank + 1) + " of " + str(size) + " on " + str(name))

    out_lines = []
    num_lines = 0
    start = time.time()

    if rank == 0:
        print(paste("Splitting", file_name))
        with open(file_name) as file:
            all_lines = file.readlines()
        input_chunks = np.array_split(all_lines, size)
    else:
        input_chunks = None

    if rank == 0:
        print(paste("Scattering", file_name))
    chunk = comm.scatter(input_chunks, root=0)
    if rank == 0:
        paste("Processing chunks")
    for line in chunk:
        out_lines.append(process_line(line))
        num_lines = num_lines + 1
    comm.barrier()

    if rank == 0:
        for node in range(1, size):
            comm.send("go", dest=node)
            num_lines = num_lines + int(comm.recv(source=node))
        print("Gathering chunks")
    else:
        comm.recv(source=0)
        comm.send(num_lines, dest=0)
    comm.barrier()

    gathered_chunks = comm.gather(out_lines, root=0)

    if rank == 0:
        print("Writing lines to CSV")
        for chunk in gathered_chunks:
            for line in chunk:
                write_row_to_csv(line, out_file_name)
        end = time.time()
        proc_time = end - start
        print(paste("Processed", num_lines, "lines in", round(proc_time, 2), "seconds at an average",
                    round(num_lines / proc_time), "lines/sec"))
