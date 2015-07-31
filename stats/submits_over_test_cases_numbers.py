from visitor import Visitor


class SubmitsOverTestCasesNumbers(Visitor):
    def __init__(self):
        super().__init__()
        self.number_of_submits_by_number_of_runs_by_problem_id = {}

    def update_submit(self, submit):
        runs_number = len(submit.runs)
        if submit.problem_id in self.number_of_submits_by_number_of_runs_by_problem_id:
            if runs_number in self.number_of_submits_by_number_of_runs_by_problem_id[submit.problem_id]:
                self.number_of_submits_by_number_of_runs_by_problem_id[submit.problem_id][runs_number] += 1
            else:
                self.number_of_submits_by_number_of_runs_by_problem_id[submit.problem_id][runs_number] = 1

        else:
            self.number_of_submits_by_number_of_runs_by_problem_id[submit.problem_id] = {}

    def pretty_print(self):
        return str(self.number_of_submits_by_number_of_runs_by_problem_id)

classname = "SubmitsOverTestCasesNumbers"
