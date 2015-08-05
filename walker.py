from os import walk
from os.path import join
from os.path import dirname


class Walker:
    # @staticmethod
    def walk(self, start_dir=dirname(__file__)):
        for root, dirs, files in walk(start_dir):
            for file in files:
                if file.startswith('.'):
                    continue
                file_name = join(root, file)
                with open(file_name, encoding='utf-8') as f:
                    yield f
