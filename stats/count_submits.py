from visitor import Visitor


class SubmitsCounter(Visitor):
    def __init__(self):
        super().__init__()
        self.result = dict()

    def visit(self, submit):
        self.result[submit.problem_id[1]] = self.result.get(submit.problem_id[1], 0) + 1

    def pretty_print(self):
        result = ''
        items = self.result.items()
        try:
            items = [(int(i[0]), i[1]) for i in items]
        except Exception:
            pass
        for k, v in sorted(items):
            result += 'Problem #{}: {} submit{}.\n'.format(k, v, '' if v == 1 else 's')
        return result

