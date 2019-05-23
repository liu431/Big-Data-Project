from mpi4py import MPI
import csv
import xml.sax
from bs4 import BeautifulSoup

## need to speficy that the directory to save to

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()
name = MPI.Get_processor_name()

if rank == 0:
    data = np.arange(20)
    # chunks as list of file names
    chunks = np.array_split(data, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0)

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
        print('calling startElement')
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
        print('done with row', self.row)


result = xml_to_csv(chunk)
gathered_chunks = comm.gather(result, root=0)

if rank == 0:
    final = gathered_chunks
    print(final)
    with open('final.csv', 'a') as out_f:
        for f in final:
            line = f.readline()
            out_f.write(line)

