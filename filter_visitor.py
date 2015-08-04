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
        return self.next_visitor.get_stat_data()

    def pretty_print(self):
        return self.next_visitor.pretty_print()

    def good_submit(self, submit):
        return True


class FilterByProblemVisitor(FilterVisitor):
    def good_submit(self, submit):
        if self.key == submit.problem_id[1]:
            return True
        return False


class FilterByContestVisitor(FilterVisitor):
    def good_submit(self, submit):
        if self.key == submit.problem_id[0]:
            return True
        return False


class FilterByUserVisitor(FilterVisitor):
    def good_submit(self, submit):
        if self.key == submit.user_id:
            return True
        return False


class FilterByLangVisitor(FilterVisitor):
    def good_submit(self, submit):
        if self.key == submit.lang_id:
            return True
        return False


class FilterAllCasesTestedSubmits(FilterVisitor):
    def good_submit(self, submit):
        return self.key[submit.problem_id] == len(submit.runs)


class FilterByScoringSystem(FilterVisitor):
    def good_submit(self, submit):
        return self.key.lower() == submit.scoring.lower()
