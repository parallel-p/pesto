__author__ = 'Kriuchkov'
from os import walk
from os import path
import gzip


def traverse_contest(my_dir):
    for d, dirs, files in walk(my_dir):
        for f in files:
            file_name = path.join(d, f)
            if file_name[-3:-1] + file_name[-1] == '.gz':
                current_file = gzip.open(file_name, 'r')
            else:
                current_file = open(file_name, 'r')
            yield current_file
            current_file.close()
