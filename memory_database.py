from ejudge_parse import ejudge_parse


class MemoryDatabase:
    def __init__(self, home_dir, csv_filename, parse=ejudge_parse):
        self.problems, self.submits = parse([home_dir.rstrip('\\').rstrip('/')], csv_filename)

    def get_problem(self, contest_id, problem_id):
        return self.problems[(contest_id, problem_id)]
