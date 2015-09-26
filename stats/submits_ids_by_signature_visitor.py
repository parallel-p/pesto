import random

from visitor import Visitor


class SubmitsIdsBySignatureVisitor(Visitor):
    min_submits = 0

    def __init__(self):
        self.result = dict()
        self.sample_count = 10

    def visit(self, submit):
        if submit.runs_results not in self.result:
            self.result[submit.runs_results] = [1, [submit.submit_id]]
        else:
            self.result[submit.runs_results][0] += 1
            if len(self.result[submit.runs_results][1]) > self.sample_count:
                if random.randint(0, self.result[submit.runs_results][0]) < self.sample_count:
                    self.result[submit.runs_results][1][random.randint(0, self.sample_count - 1)] = submit.submit_id
            else:
                self.result[submit.runs_results][1].append(submit.submit_id)


    def get_stat_data(self):
        for arr in self.result.values():
            arr[1].sort(key=int)
        return self.result

    def pretty_print(self):
        temp_data = list(self.get_stat_data().items())
        temp_data.sort(key=lambda x: (-len(x[0]), -x[1][0], x[1][1]))

        total = sum(i[1][0] for i in temp_data)
        answer = ['Total submits: {}'.format(total)]
        for signature, sabmits_num_and_samp in temp_data:
            if sabmits_num_and_samp[0] >= self.min_submits:
                answer.append('{} submits: {}\n  Samples: {}'.format(sabmits_num_and_samp[0], signature,
                                                                                 ', '.join(sabmits_num_and_samp[1])))
        answer.append('')

        return '\n'.join(answer)
