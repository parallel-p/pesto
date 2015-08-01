from visitor import Visitor


class VisitorFactory:
    def create(self, key):
        return Visitor()
