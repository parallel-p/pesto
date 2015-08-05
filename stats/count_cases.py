from cases_stats import CasesStats


class CasesCounter(CasesStats):
    def __init__(self, problems):
        super().__init__(problems)
        self.result = dict()

    def get_stat_data(self):
        for problem in self.problems:
            self.result[problem.problem_id] = len(problem.cases)
        return self.result

    def __str__(self):
        result = ''
        for problem_id, cases in sorted(self.result.items()):
            result += 'Contest #{0} Problem #{1}: {2} case(s)\n'.format(problem_id[0],
                                                                        problem_id[1],
                                                                        cases)
        return result
