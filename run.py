class Run:
    def __init__(self, problem, submit_id, case_id, outcome):
        self.problem = problem
        self.submit_id = submit_id
        self.case_id = case_id
        self.outcome = outcome

    def __str__(self):
        result = "Case #{0} Outcome {1}".format(str(self.case_id), str(self.outcome))
        return result