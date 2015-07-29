class Submit:

    def __init__(self, submit_id, problem, user_id, runs, outcome):
        self.problem = problem
        self.submit_id = submit_id
        self.runs = runs
        self.outcome = outcome
        self.user_id = user_id

    def __str__(self):
        return(("Submit: {0}; Result: {1}; User id: {2}; Runs: {3}.").format(self. submit_id, self.outcome, self.user_id, (", ").join(self.runs)))