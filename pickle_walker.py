from os import walk
from os.path import join
import pickle


def pickle_walker(start_dir):
    for root, dirs, files in walk(start_dir):
        for file in files:
            if not file.endswith('.pickle'):
                continue

            file_name = join(root, file)
            arr = []
            try:
                with open(file_name, 'rb') as file:
                    arr = pickle.load(file)
            except pickle.UnpicklingError:
                pass

            for submit in arr:
                yield submit
