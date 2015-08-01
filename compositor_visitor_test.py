import unittest
from compositor_visitor import CompositorVisitor
from visitor import FakeVisitor


class FunctionTesting(unittest.TestCase):
    def test_empty_output(self):
        comp_visitor = CompositorVisitor()
        self.assertEqual(comp_visitor.pretty_print(), "")

    def test_one_visitors(self):
        visitor = FakeVisitor()
        comp_visitor = CompositorVisitor(visitor)
        comp_visitor.visit(10)
        self.assertEqual(comp_visitor.pretty_print(), "1")

    def test_two_visitors(self):
        visitors = []
        for i in range(2):
            visitors.append(FakeVisitor())

        comp_visitor = CompositorVisitor(*visitors)
        visitors[0].visit(10)
        comp_visitor.visit(10)
        self.assertEqual(comp_visitor.pretty_print(), "2\n\n1")


if __name__ == "__main__":
    unittest.main()
