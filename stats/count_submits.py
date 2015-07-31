from visitor import Visitor


class SubmitsCounter(Visitor):
    def __init__(self):
        super().__init__()
        self.result = dict()

    def update_submit(self, submit):
        if str(submit.problem_id) not in self.result:
            self.result[submit.problem_id] = 1
        else:
            self.result[submit.problem_id] += 1

    def pretty_print(self):
        result = ''
        for k, v in sorted(self.result.items()):
            result += 'Problem #{}: {} submits.\n'.format(k, v)
        return result

classname = 'SubmitsCounter'
