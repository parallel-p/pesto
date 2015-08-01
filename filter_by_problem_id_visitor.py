from visitor import Visitor


class FilterByProblemIdVisitor(Visitor):
    def __init__(self, problem_id, visitor):
        self.target_visitor = visitor
        self.problem_id = problem_id

    def visit(self, submit):
        if submit.problem_id[1] == self.problem_id:
            self.target_visitor.visit(submit)

    def get_stat_data(self):
        return self.target_visitor.get_stat_data()

    def pretty_print(self):
        return self.target_visitor.pretty_print()
