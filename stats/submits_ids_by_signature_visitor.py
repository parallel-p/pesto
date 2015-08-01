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
        answer = []
        for signature in self.result:
            answer.append('{}: {} submits found.'.format(signature, len(self.result[signature])))
        return '\n'.join(answer)


classname = 'SubmitsIdsBySignatueVisitor'