from cases_stats import CasesStats


class FindElephants(CasesStats):
    def __init__(self, problems):
        self.result = []
        for problem in problems:
            is_elephant = True
            for hash_io in problem.cases_io:
                if hash_io[0] is None or hash_io[0] == "" or hash_io[0] != hash_io[1]:
                    is_elephant = False
                    break
            if is_elephant:
                self.result.append(problem)

        self.result.sort(key=lambda x: x.problem_id)

    def get_stat_data(self):
        return self.result

    def __str__(self):
        resulting_string = 'There are {} elephants.\n'.format(len(self.result))
        for problem in self.result:
            resulting_string += 'Problem {} from contest {} is an elephant.\n'.format(
                problem.name, problem.problem_id[0])
        return resulting_string
