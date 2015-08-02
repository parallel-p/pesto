from visitor import Visitor


class FilterVisitor(Visitor):
    def __init__(self, next_visitor, key):
        super().__init__()
        self.next_visitor = next_visitor
        self.key = key

    def visit(self, submit):
        if self.good_submit(submit):
           self.next_visitor.visit(submit)

    def get_stat_data(self):
        return {'key':self.key}

    def pretty_print(self):
        return "Key:" + str(self.key)

    def good_submit(self, submit):
        return True


class FilterByProblemVisitor(FilterVisitor):
    def good_submit(self, submit):
        return self.key == submit.problem_id


class FilterByUserVisitor(FilterVisitor):
    def build_key(self, submit):
        return self.key == submit.user_id
