class FilterByProblemIdVisitor():
    def __init__(self, problem_id, visitor):
        self.target_visitor = visitor
        self.problem_id = problem_id

    def update_submit(self, submit):
        if submit.problem == self.problem_id:
            self.target_visitor.update_submit(submit)