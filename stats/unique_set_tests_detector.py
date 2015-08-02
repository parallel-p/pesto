from visitor import Visitor


class UniqueSetTestsDetector(Visitor):
    def __init__(self):
        #submits_number by uniqum_runs_results by contest_problem_id
        self.result = dict()

    def visit(self, submit):
        id = submit.problem_id
        if id in self.result:
            if submit.runs_results in self.result[id]:
                self.result[id][submit.runs_results][1] += 1
            else:
                self.result[id][submit.runs_results] = [[run.outcome for run in submit.runs], 1]
        else:
            self.result[id] = {submit.runs_results:[[run.outcome for run in submit.runs], 1]}

    def get_sort_result(self):
        return sorted(self.result.items())

    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        sorted_result = self.get_sort_result()
        prettty_result = []

        for problem_id_and_runs in sorted_result:
            prettty_result.append("***")
            prettty_result.append("contest_problem #" + '_'.join(problem_id_and_runs[0]))

            for uniqum_result in sorted(problem_id_and_runs[1]):
                runs_res_in_string = ' '.join(self.result[problem_id_and_runs[0]][uniqum_result][0])
                submits_number = self.result[problem_id_and_runs[0]][uniqum_result][1]

                prettty_result.append("  Run result:{0}\n   Submits count:{1}\n".format(runs_res_in_string, submits_number))
        return '\n'.join(prettty_result)

