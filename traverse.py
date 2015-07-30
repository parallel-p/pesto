from os import walk
from os.path import join
from gzip import open as gzip_open


def traverse_contest(first_dir):
    for root, dirs, files in walk(first_dir):
        for file in files:
            if file.startswith('.'):
                continue
            file_name = join(root, file)
            if file_name.endswith('.gz'):
                try:
                    current_file = gzip_open(file_name)
                except OSError:  # invalid .gz
                    continue
            else:
                current_file = open(file_name, encoding='utf-8')
            yield current_file
            current_file.close()
