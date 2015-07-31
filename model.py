class Problem:
    def __init__(self, contest_id, problem_id, case_ids):
        """
        :type contest_id: str or int
        :type problem_id: str or int
        :type case_ids: list
        """
        self.contest_id = contest_id
        self.problem_id = problem_id
        self.case_ids = case_ids

    def __str__(self):
        return 'Contest #{0} Problem #{1}\nCases: {2}'.format(self.contest_id,
                                                              self.problem_id,
                                                              self.case_ids)

    def get_submits(self, database):  # Returns all submits for particular problem
        for submit in database.submits:
            if submit.problem.problem_id == self.problem_id:
                yield submit



class Submit:
    def __init__(self, submit_id, problem_id, user_id, runs, outcome):

        self.problem_id = problem_id
        self.submit_id = submit_id
        self.runs = runs
        self.outcome = outcome
        self.user_id = user_id
        self.runs_results = ''.join([str(run.outcome) for run in self.runs])

    def __str__(self):
        return "Submit: {0}; Result: {1}; User id: {2}; Runs: {3}.".format(self.submit_id, self.outcome,
                                                                           self.user_id,
                                                                           ", ".join([str(run)
                                                                                      for run in self.runs]))


class Run:
    def __init__(self, problem_id, submit_id, case_id, outcome, contest_id):
        self.problem_id = problem_id
        self.contest_id = contest_id
        self.submit_id = submit_id
        self.case_id = case_id
        self.outcome = outcome

    def __str__(self):
        result = "Contest #{0} Case #{1} Outcome {2}".format(self.contest_id,
                                                             str(self.case_id),
                                                             str(self.outcome))
        return result

    def __repr__(self):
        return str(self)
