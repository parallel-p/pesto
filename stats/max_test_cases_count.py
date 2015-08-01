from visitor import Visitor
import csv


class MaxTestCasesCount(Visitor):
    def __init__(self, file_name):
        self.file_name = file_name
        self.max_test_cases_number_by_problem_id = dict()

    def visit(self, submit):
        if submit.problem_id in self.max_test_cases_number_by_problem_id:
            self.max_test_cases_number_by_problem_id[submit.problem_id] = max(self.max_test_cases_number_by_problem_id[submit.problem_id], len(submit.runs))
        else:
            self.max_test_cases_number_by_problem_id[submit.problem_id] = len(submit.runs)

    def get_stat_data(self):
        csv_file = open(self.file_name, "w")
        for problem_id in self.max_test_cases_number_by_problem_id:
            print("\"{0}\";\"{1}\";\"{2}\"".format(problem_id[0], problem_id[1], self.max_test_cases_number_by_problem_id[problem_id]), file=csv_file, sep=";")

        return self.max_test_cases_number_by_problem_id

classname = "MaxTestCasesCount"