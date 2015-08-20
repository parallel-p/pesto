from visitor import Visitor
import operator


class SubmitsOverTestCasesNumbers(Visitor):
    def __init__(self):
        super().__init__()
        self.result = {}

    def visit(self, submit):
        runs_number = len(submit.runs)
        if submit.problem_id in self.result:
            self.result[submit.problem_id][runs_number] = self.result[submit.problem_id].get(runs_number, 0) + 1
        else:
            self.result[submit.problem_id] = {runs_number: 1}

    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        data_dict = self.result
        data_list = sorted(data_dict.items())
        result = ''
        for problem in data_list:
            problem_id, data = problem
            test_cases, submit_numbers = list(data.keys()), list(data.values())

            line_multiplier = 100 / max(submit_numbers)
            result += ('-------------\n'
                       'Problem #{0}\n'
                       '-------------\n'.format(problem_id))
            for i in range(len(test_cases)):
                result += '{0:{width}} {1} {2}\n'.format(test_cases[i],
                                                         '#' * int(submit_numbers[i]
                                                                   * line_multiplier),
                                                         submit_numbers[i], width=5)

        return result

