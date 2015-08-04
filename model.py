class Submit:
    def __init__(self, submit_id, problem_id, user_id, lang_id, runs, outcome, scoring):

        self.problem_id = problem_id
        self.submit_id = submit_id
        self.runs = runs
        self.outcome = outcome
        self.user_id = user_id
        self.lang_id = lang_id
        self.scoring = scoring
        self.runs_results = ''.join([str(run.outcome) for run in self.runs])

    def __str__(self):
        return "Submit: {0}; Result: {1}; User id: {2}; Runs: {3}.".format(self.submit_id, self.outcome,
                                                                           self.user_id,
                                                                           ", ".join([str(run)
                                                                                      for run in self.runs]))


class Run:
    def __init__(self, problem_id, submit_id, case_id, outcome):
        self.problem_id = problem_id
        self.submit_id = submit_id
        self.case_id = case_id
        self.outcome = outcome

    def __str__(self):
        result = "Case #{0} Outcome {1}".format(str(self.case_id), str(self.outcome))
        return result

    def __repr__(self):
        return str(self)
