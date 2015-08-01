from visitor import Visitor


class ShardingVisitor(Visitor):
    def __init__(self, factory):
        super().__init__()
        self.visitors = dict()
        self.factory = factory

    def visit(self, submit):
        key = self.build_key(submit)
        if key not in self.visitors:
            self.visitors[key] = self.factory.create(key)
        self.visitors[key].visit(submit)

    def get_stat_data(self):
        result = []
        for key_visitor in sorted(self.visitors.items()):
            result.append((key_visitor[0], key_visitor[1].get_stat_data()))
        return result

    def pretty_print(self):
        if len(self.visitors) == 0:
            return ""
        else:
            return "\n\n".join([" ".join(["Key:", str(key_visitor[0]), key_visitor[1].pretty_print()]) for key_visitor in sorted(self.visitors.items())])

    def build_key(self, submit):
        return str(submit)


class ShardingByProblemVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id


class ShardingByContestVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id[0]


class ShardingByUserVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.user_id
