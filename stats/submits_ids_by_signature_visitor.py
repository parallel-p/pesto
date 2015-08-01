from visitor import Visitor


class SubmitsIdsBySignatueVisitor(Visitor):
    def __init__(self):
        self.result = dict()

    def visit(self, submit):
        if submit.runs_results not in self.result:
            self.result[submit.runs_results] = [submit.problem_id]
        else:
            self.result[submit.runs_results].apend(submit.problem_id)

    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        result = []
        for singnature in self.result:
            result.append("Signatue:", str(singnature), "Submits ids:",  ''.join(self.result))


classname = 'SubmitsIdsBySignatueVisitor'