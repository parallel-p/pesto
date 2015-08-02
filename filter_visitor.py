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
        return {'key':self.key, "next_visitor_stat":self.get_stat_data()}

    def pretty_print(self):
        return "Key:{0}; Next visitor stat:{1}".format(str(self.key), self.next_visitor.pretty_print)

    def good_submit(self, submit):
        return True


class FilterByProblemVisitor(FilterVisitor):
    def good_submit(self, submit):
        return self.key == submit.problem_id[1]


class FilterByContestVisitor(FilterVisitor):
    def good_submit(self, submit):
        return self.key == submit.problem_id[0]


class FilterByUserVisitor(FilterVisitor):
    def good_submit(self, submit):
        return self.key == submit.user_id

