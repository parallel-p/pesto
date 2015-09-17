from cases_stats import CasesStats


class CasesCounter(CasesStats):
    def __init__(self, problems):
        super().__init__(problems)
        self.result = dict()
        for problem in self.problems:
            self.result[problem.problem_id] = len(problem.cases)

    def get_stat_data(self):
        return self.result

    def __str__(self):
        result = ''
        for problem_id, cases in sorted(self.result.items(), key=lambda x: (int(x[0][0]), int(x[0][1]))):
            result += 'Contest #{0} Problem #{1}: {2} case{3}\n'.format(problem_id[0].rjust(6, '0'),
                                                                        problem_id[1],
                                                                        cases, '' if cases == 1 else 's')
        return result
