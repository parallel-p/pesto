import random
from visitor import Visitor


class SubmitsIdsBySignatureVisitor(Visitor):
    def __init__(self):
        self.result = dict()
        self.submits_number = 0
        self.sample_submits_ids = []

    def visit(self, submit):
        self.submits_number += 1
        if submit.runs_results not in self.result:
            self.result[submit.runs_results] = [1, [submit.submit_id]]
        else:
            self.result[submit.runs_results][0] += 1
            if len(self.result[submit.runs_results][1]) > 10:
                if random.randint(0, self.submits_number) == 5:
                    self.result[submit.runs_results][1][random.randint(0, 9)] = submit.submit_id
            else:
                self.result[submit.runs_results][1].append(submit.submit_id)


    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        temp_data = list(self.result.items())
        temp_data.sort(key=lambda x:(-len(x[0]), -x[1][0], x[1][1]))

        answer = []
        for signature, sabmits_num_and_samp in temp_data:
            answer.append('{}: {} submits found.\nSubmits ids samples:{}'.format(signature, sabmits_num_and_samp[0], sabmits_num_and_samp[1]))

        return '\n'.join(answer)

    def _sortByTestCassesCount(element):
        return (len(element))
