class EjudgeDBEntry:
    def __init__(self, problem_id, user_id, lang_id):
        self.problem_id = problem_id
        self.user_id = user_id
        self.lang_id = lang_id

class EjudgeDB:
    def __init__(self, csv_filename, contest_ids=None):
        self.data = {}
        with open(csv_filename) as csv_file:
            for line in csv_file:
                ejudge_run_id, contest_id, user_id, problem_id, lang_id, status = map(lambda x: x[1:-1], line.split(';'))
                if contest_ids is None or contest_id in contest_ids:
                    self.data[(contest_id, ejudge_run_id)] = EjudgeDBEntry(problem_id, user_id, lang_id)
    
    def get_problem_id(self, contest_id, ejudge_run_id):
        return self.data[(contest_id, ejudge_run_id)].problem_id
    
    def get_user_id(self, contest_id, ejudge_run_id):
        return self.data[(contest_id, ejudge_run_id)].user_id
    
    def get_lang_id(self, contest_id, ejudge_run_id):
        return self.data[(contest_id, ejudge_run_id)].lang_id    