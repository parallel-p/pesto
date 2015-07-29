__author__ = 'Kriuchkov'
from os import walk
from os.path import join
from gzip import open as gzip_open


def traverse_contest(first_dir):
    for root, dirs, files in walk(first_dir):
        for f in files:
            if f[0] == '.':
                continue
            file_name = join(root, f)
            if file_name.endswith('.gz'):
                current_file = gzip_open(file_name, encoding='utf-8')
            else:
                current_file = open(file_name, encoding='utf-8')
            yield current_file
            current_file.close()
