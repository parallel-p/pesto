from visitor import Visitor


class MaxTestCasesCount(Visitor):
    def __init__(self):
        self.result = 0

    def visit(self, submit):
        self.result = max(self.result, len(submit.runs))

    def get_stat_data(self):
        return self.result

    def pretty_print(self):
        return 'Test cases:{}'.format(self.result)




