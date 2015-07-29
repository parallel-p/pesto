__author__ = 'Daniil Konovalenko'


class Problem:
    def __init__(self, contest_id, problem_id, case_ids):
        self.contest_id = contest_id
        self.problem_id = problem_id
        self.case_ids = case_ids

    def __str__(self):
        return 'Contest #{0} Problem #{1}\nCases: {2}'.format(self.contest_id,
                                                              self.problem_id,
                                                              str(self.case_ids))
