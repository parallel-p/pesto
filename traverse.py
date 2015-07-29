__author__ = 'Kriuchkov'
from os import walk
from os.path import join
import gzip


def traverse_contest(my_dir):
    for root, dirs, files in walk(my_dir):
        for f in files:
            file_name = join(root, f)
            if file_name.endswith('.gz'):
                current_file = gzip.open(file_name, 'r')
            else:
                current_file = open(file_name, 'r')
            yield current_file
            current_file.close()
