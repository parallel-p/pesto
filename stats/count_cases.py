from visitor import Visitor


class CasesCounter(Visitor):
    def __init__(self):
        super().__init__()
        self.result = {}
    
    def visit(self, submit):
        if str(submit.problem_id[1]) not in self.result or len(submit.runs) > self.result[str(submit.problem_id[1])]:
            self.result[str(submit.problem_id[1])] = len(submit.runs)
    
    def pretty_print(self):
        result = ''
        for k, v in sorted(self.result.items()):
            result += 'Problem #{}: {} cases.\n'.format(k, v)        
        return result
