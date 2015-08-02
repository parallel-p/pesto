from visitor import Visitor
import csv


class MaxTestCasesCount(Visitor):
    def __init__(self):
        self.max_test_cases_number_by_problem_id = dict()

    def visit(self, submit):
        if submit.problem_id in self.max_test_cases_number_by_problem_id:
            self.max_test_cases_number_by_problem_id[submit.problem_id] = max(self.max_test_cases_number_by_problem_id[submit.problem_id], len(submit.runs))
        else:
            self.max_test_cases_number_by_problem_id[submit.problem_id] = len(submit.runs)

    def get_stat_data(self):
        return self.max_test_cases_number_by_problem_id

