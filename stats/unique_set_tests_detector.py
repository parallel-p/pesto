from visitor import Visitor
import operator


class UniqueSetTestsDetector(Visitor):
    def __init__(self):
        self.submits_number_by_uniqum_runs_results_by_contest_problem_id = dict()

    def visit(self, submit):
        probl_id = submit.problem_id
        cont_id = submit.contest_id
        id = cont_id + "_" + probl_id
        if id in self.submits_number_by_uniqum_runs_results_by_contest_problem_id:
            if submit.runs_results in self.submits_number_by_uniqum_runs_results_by_contest_problem_id[id]:
                self.submits_number_by_uniqum_runs_results_by_contest_problem_id[id][submit.runs_results][1] += 1
            else:
                self.submits_number_by_uniqum_runs_results_by_contest_problem_id[id][submit.runs_results] = [[run.outcome for run in submit.runs], 1]
        else:
            self.submits_number_by_uniqum_runs_results_by_contest_problem_id[id] = dict()

    def get_sort_result(self):
        return sorted(self.submits_number_by_uniqum_runs_results_by_contest_problem_id.items(), key=operator.itemgetter(0))

    def get_stat_data(self):
        return self.submits_number_by_uniqum_runs_results_by_contest_problem_id

    def pretty_print(self):
        sorted_result = self.get_sort_result()
        prettty_result = []
        for problem_id_and_runs in sorted_result:
            prettty_result.append("***")
            prettty_result.append("contest_problem #" + problem_id_and_runs[0])
            for uniqum_result in problem_id_and_runs[1]:
                runs_res_in_string = ' '.join(self.submits_number_by_uniqum_runs_results_by_contest_problem_id[problem_id_and_runs[0]][uniqum_result][0])
                submits_number = self.submits_number_by_uniqum_runs_results_by_contest_problem_id[problem_id_and_runs[0]][uniqum_result][1]
                prettty_result.append("  Run result:{0}\n   Submits count:{1}\n".format(runs_res_in_string, submits_number))
        return '\n'.join(prettty_result)



classname = 'UniqueSetTestsDetector'