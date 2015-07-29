class Submit:

    def __init__(self, sub_id, problem, user_id, runs, outcome):
        self.problem = problem
        self.submit_id = sub_id
        self.runs = runs
        self.outcome = outcome
        self.user_id = user_id

    def __str__(self):
        submit_id = "Submit:" + self. submit_id
        test_result = "; Result:" + self.outcome
        usr_id = "; User ID:" + self.user_id
        runs_info = ";\nRuns:\n" + " \n".join(self.runs)

        return(submit_id + test_result + user_id + runs_info)

