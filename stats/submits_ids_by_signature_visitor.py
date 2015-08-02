import random
from visitor import Visitor


class SubmitsIdsBySignatueVisitor(Visitor):
    def __init__(self):
        self.result = dict()

    def visit(self, submit):
        if submit.runs_results not in self.result:
            self.result[submit.runs_results] = [submit.submit_id]
        else:
            self.result[submit.runs_results].append(submit.submit_id)

    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        temp_data = list(self.result.items())
        for i in range(len(temp_data)):
            temp_data[i] = (len(temp_data[i][1]), temp_data[i][0])
        answer = []
        for submits, signature in sorted(temp_data):
            sample_submits_ids = random.sample(range(submits), min(10, submits))
            sample_sabmits = [self.result[signature][i] for i in sample_submits_ids]
            answer.append('{}: {} submits found.\nSubmits ids samples:{}'.format(signature, submits, str(sorted(sample_sabmits))))
        return '\n'.join(answer)


classname = 'SubmitsIdsBySignatueVisitor'