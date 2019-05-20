from textblob import TextBlob
import csv
import sys


def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity > 0


def next_blurb(filename, col_index):
    with open(filename) as csv_file:
        csv_rows = csv.reader(csv_file, delimiter=',')
        for row in csv_rows:
            yield row[col_index]


if __name__ == '__main__':
    file_path = sys.argv[1]
    col_index = int(sys.argv[2])
    for blurb in next_blurb(file_path, col_index):
        if get_sentiment(blurb):
            print("Positive: " + blurb)
        else:
            print("Negative: " + blurb)
