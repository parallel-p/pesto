import os.path


class MemoryDatabase:
    def __init__(self, home_dir, traverse_contest, get_submit):
        self.submits = []
        self.problems = dict()
        self.home_dir = home_dir.rstrip(os.path.sep)
        self.traverse_contest = traverse_contest  # function
        self.get_submit = get_submit  # function
        self.init_database()

    def init_database(self):
        try:
            contest_id = int(os.path.basename(self.home_dir))  # directory name
        except ValueError:
            contest_id = None
        for file in self.traverse_contest(self.home_dir):
            self.submits.append(self.get_submit(file, self, contest_id))

    # called from get_submit
    def problem_exists(self, contest_id, problem_id):
        return (contest_id, problem_id) in self.problems

    # called from get_submit
    def add_problem(self, contest_id, problem_id, problem):
        self.problems[(contest_id, problem_id)] = problem
