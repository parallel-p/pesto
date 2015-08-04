class CaseCounter:

    def __init__(self, problem_list):
        self.cases_count = dict()
        for i in problem_list:
            self.cases_count[i.problem_id] = len(i.cases)

    def get_cases_number(self, problem_id):
        return self.cases_count.get(problem_id, None)
