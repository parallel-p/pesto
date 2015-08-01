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
            temp_data[i] = (temp_data[i][1], len(temp_data[i][0]))
        answer = []
        for submits, signature in sorted(temp_data):
            answer.append('{}: {} submits found.'.format(signature, len(submits)))
        return '\n'.join(answer)


classname = 'SubmitsIdsBySignatueVisitor'