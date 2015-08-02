from visitor import Visitor


class MaxTestCasesCount(Visitor):
    def __init__(self):
        #max_test_cases_number by problem_id
        self.result = dict()

    def visit(self, submit):
        if submit.problem_id in self.result:
            self.result[submit.problem_id] = max(self.result[submit.problem_id], len(submit.runs))
        else:
            self.result[submit.problem_id] = len(submit.runs)

    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        sorted_res = sorted(list(self.result.items()))
        answer = ["***"]

        for problem_id, submits_num in sorted_res:
            answer.append("\nContest:{}; Problem {}; Test cases number:{}\n".format(problem_id[0], problem_id[1], submits_num))

        return ''.join(answer)




