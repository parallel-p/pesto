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
        for visitor in self.visitors.values():
            result.append(visitor.get_stat_data())
        return result

    def pretty_print(self):
        if len(self.visitors) == 0:
            return ""
        else:
            return "\n\n".join([visitor.pretty_print() for visitor in self.visitors.values()])

    def build_key(self, submit):
        return submit