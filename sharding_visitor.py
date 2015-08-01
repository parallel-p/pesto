from visitor import Visitor

class ShardingVisitor(Visitor):
    def __init__(self, factory):
        self.visitors = dict()
        self.factory = factory

    def update_submit(self, submit):
        key = build_key(submit)
        if key not in self.visitors() :
            self.visitors[key] = self.factory.create(key)

    def get_stat_data(self):
        result = []
        for visitor in self.visitors.values():
            result.append(visitor.get_stat_data())
        return result

    def pretty_print(self):
        if len(self.visitors) == 0:
            return ""
        else:
            return "\n\n".join([visitor.pretty_print() for visitor in self.visitors])

    def build_key(self, submit):
        return None