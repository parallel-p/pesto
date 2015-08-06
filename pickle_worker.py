from walker import Walker
from os import walk
from os.path import join
import pickle


class PickleWorker(Walker):
    def walk(self, start_dir):
        for root, dirs, files in walk(start_dir):
            for file in files:
                if not file.endswith('.pickle'):
                    continue

                file_name = join(root, file)
                yield file_name