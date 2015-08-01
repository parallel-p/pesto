from visitor import Visitor


class VisitorFactory:
    @staticmethod
    def create(key):
        return Visitor()
