from visitor import Visitor


class ElectorVisitor(Visitor):
    def __init__(self, factory):
        super().__init__()
        self.factory = factory
        self.key = None
        self.visitor = None

    def visit(self, submit):
        key = self.build_key(submit)
        if self.is_key_better(key):
            self.key = key
            self.visitor = self.factory.create(key)
        if key == self.key:
            self.visitor.visit(submit)

    def build_key(self, submit):
        return str(submit)

    def is_key_better(self, key):
        return self.key is None or key > self.key

    def pretty_print(self):
        return self.visitor.pretty_print() if self.visitor is not None else ''

    def get_stat_data(self):
        return self.visitor.get_stat_data() if self.visitor is not None else {}


class ElectorByMaxCasesVisitor(ElectorVisitor):
    def build_key(self, submit):
        return len(submit.runs)
