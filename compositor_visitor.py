from visitor import Visitor


class CompositorVisitor(Visitor):
    def __init__(self, *visitors):
        super().__init__()
        self.visitors = list(visitors)

    def visit(self, update_submit):
        for visitor in self.visitors:
            visitor.visit(update_submit)

    def pretty_print(self):
        if len(self.visitors) == 0:
            return ""
        else:
            return "\n\n".join([visitor.pretty_print() for visitor in self.visitors])

    def get_stat_data(self):
        result = []
        for visitor in self.visitors.values():
            result.append(visitor.get_stat_data())
        return result