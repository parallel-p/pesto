class Submit:

    def __init__(self, sub_id, problem, user, runs, outcome):
        self.problem = problem
        self.submit_id = sub_id
        self.runs = runs
        self.outcome = outcome
        self.user = user

    def __str__(self):
        submit_id = "Submit id:" + self. submit_id
        test_result = "; Result:" + self.outcome
        usr_info = "; User info:" + self.user
        runs_info = ";\nRuns:\n" + " \n".join(self.runs)

        return(submit_id + test_result + usr_info + runs_info)

