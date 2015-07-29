import os.path
from traverse import traverse_contest
from ejudge_get_submit import ejudge_get_submit
from ejudgedb import EjudgeDB


class MemoryDatabase:
    def __init__(self, home_dir, csv_filename=None):
        self.submits = []
        self.problems = dict()
        self.home_dir = home_dir.rstrip('\\').rstrip('/')
        if csv_filename is not None:
            self.database = EjudgeDB(csv_filename)
        else:
            self.database = None
        self.init_database()

    def get_problem_id(self, contest_id, submit_id):
        if self.database is not None:
            return self.database.get_problem_id(contest_id, submit_id)
        return None

    def get_user_id(self, contest_id, submit_id):
        if self.database is not None:
            return self.database.get_user_id(contest_id, submit_id)
        return None

    def get_lang_id(self, contest_id, submit_id):
        if self.database is not None:
            return self.database.get_lang_id(contest_id, submit_id)
        return None

    def init_database(self):
        try:
            contest_id = str(int(os.path.basename(self.home_dir)))  # directory name
        except ValueError:
            contest_id = None
        for file in traverse_contest(self.home_dir):
            try:
                submit = ejudge_get_submit(file, self, contest_id)
                if submit is not None:
                    self.submits.append(submit)
            except UnicodeError:
                pass

    # called from get_submit
    def problem_exists(self, contest_id, problem_id):
        return (str(contest_id), str(problem_id)) in self.problems

    # called from get_submit
    def add_problem(self, contest_id, problem_id, problem):
        self.problems[(str(contest_id), str(problem_id))] = problem

    # called from get_submit
    def get_problem(self, contest_id, problem_id):
        return self.problems[(str(contest_id), str(problem_id))]
