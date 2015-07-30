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
            _result = "Submit: {0}; Result: {1}; User id: {2}; Runs: {3}.".format(self.submit_id, self.outcome, self.user_id, (", ").join([str(run) for run in self.runs]))
        else:
            _result = "Submit: {0}; Result: {1}; User id: {2}; No Runs.".format(self.submit_id, self.outcome, self.user_id)
        return _result
