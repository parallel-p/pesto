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
        result = list()
        for submit in database.submits:
            if submit.problem.problem_id == self.problem_id:
                result.append(submit)
        return result


class Submit:
    def __init__(self, submit_id, problem, user_id, runs, outcome):

        self.problem = problem
        self.submit_id = submit_id
        self.runs = runs
        self.outcome = outcome
        self.user_id = user_id
        self.runs_results = ''.join([str(run.outcome) for run in self.runs])

    def __str__(self):
        if len(self.runs) != 0:
            _result = "Submit: {0}; Result: {1}; User id: {2}; Runs: {3}.".format(self.submit_id, self.outcome,
                                                                                  self.user_id,
                                                                                  ", ".join([str(run)
                                                                                             for run in self.runs]))
        else:
            _result = "Submit: {0}; Result: {1}; User id: {2}; No Runs.".format(self.submit_id, self.outcome,
                                                                                self.user_id)
        return _result


class Run:
    def __init__(self, problem, submit_id, case_id, outcome):
        self.problem = problem
        self.submit_id = submit_id
        self.case_id = case_id
        self.outcome = outcome

    def __str__(self):
        result = "Case #{0} Outcome {1}".format(str(self.case_id), str(self.outcome))
        return result
