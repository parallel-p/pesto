import unittest
from compositor_visitor import CompositorVisitor
from visitor import Visitor


class FakeVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.result = 0

    def visit(self, submit):
        self.result += submit

    # Returns ready for print string of result data
    def pretty_print(self):
        return str(self.result)


class FunctionTesting(unittest.TestCase):
    def test_empty_output(self):
        comp_visitor = CompositorVisitor()
        self.assertEqual(comp_visitor.pretty_print(), "")

    def test_one_visitors(self):
        visitor = FakeVisitor()
        comp_visitor = CompositorVisitor(visitor)
        comp_visitor.visit(10)
        self.assertEqual(comp_visitor.pretty_print(), "10")

    def test_two_visitors(self):
        visitors = []
        for i in range(2):
            visitors.append(FakeVisitor())

        comp_visitor = CompositorVisitor(*visitors)
        visitors[0].visit(10)
        comp_visitor.visit(10)
        self.assertEqual(comp_visitor.pretty_print(), "20\n\n10")


if __name__ == "__main__":
    unittest.main()
