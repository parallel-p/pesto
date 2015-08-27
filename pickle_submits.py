from pickle import dump, HIGHEST_PROTOCOL, PicklingError
from os import mkdir

from os.path import exists, join

from visitor import Visitor


class PickleWriter(Visitor):
    def __init__(self):
        super().__init__()
        self.transmitted_submits = 0
        self.contest_id = ""
        self.default_path = join(".", "pickle")
        self.pickle_id = None
        self.submits = []
        self.limit = 100

    def visit(self, submit):
        if submit.problem_id[0] != self.contest_id:
            if self.submits:  # if there are submits
                self.write_file()
                self.submits = []
            self.contest_id = submit.problem_id[0]
            self.transmitted_submits = 0

        self.transmitted_submits += 1
        self.submits.append(submit)
        if self.transmitted_submits % self.limit == 0:  # if 100th submit
            self.write_file()
            self.submits = []

    def write_file(self):
        if self.submits:
            if not exists(self.default_path):
                mkdir(self.default_path)
            if self.transmitted_submits % self.limit != 0:
                file_name = "pickle" + "0" * (6 - len(str(self.transmitted_submits // self.limit))) + str(
                    self.transmitted_submits // self.limit) + "_" + str(
                    self.transmitted_submits % self.limit) + ".pickle"
            else:
                file_name = "pickle" + "0" * (6 - len(str(self.transmitted_submits // self.limit))) + str(
                    self.transmitted_submits // self.limit) + ".pickle"
            path = join(self.default_path, str(self.contest_id), file_name)
            dir = join(self.default_path, str(self.contest_id))
            if not exists(dir):
                mkdir(dir)
            with open(path, "wb") as pickle_file:
                try:
                    dump(self.submits, pickle_file, HIGHEST_PROTOCOL)
                except PicklingError:
                    pass

    def close(self):
        self.write_file()
