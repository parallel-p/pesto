from cases_stats import CasesStats


class SameProblemsFinder(CasesStats):
    def __init__(self, problems):
        cases_to_problems = dict()
        for problem in problems:
            key = tuple(problem.cases)
            if key not in cases_to_problems:
                cases_to_problems[key] = [problem]
            else:
                cases_to_problems[key].append(problem)

        self.result = []
        for problems_set in cases_to_problems.values():
            if len(problems_set) > 1:
                self.result.append(sorted(problems_set, key=lambda x: x.problem_id))

        self.result.sort(key=lambda x: x[0].problem_id)

    def get_stat_data(self):
        return self.result

    def __str__(self):
        resulting_string = ''
        for problems_set in self.result:
            resulting_string += 'Problems {} are same.\n'.format(', '.join(
                ['"{}" from contest {}'.format(problem.name, problem.problem_id[0]) for problem in problems_set]))
        return resulting_string
