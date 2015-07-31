import unittest
from compositor_visitor import CompositorVisitor
from visitor import Visitor

class FakeVisitor(Visitor):
    def __init__(self):
        self.result = 0

    def update_submit(self, submit):
        self.result += submit

    #Returns ready for print string of result data
    def get_stat_data(self):
        return str(self.result)


class FunctionTesting(unittest.TestCase):
    def test_empty_output(self):
        comp_visitor = CompositorVisitor()
        self.assertEqual(comp_visitor.get_stat_data(), "")

    def test_2visitors(self):
        visitors = []
        for i in range(2):
            visitors.append(FakeVisitor())

        comp_visitor = CompositorVisitor(*visitors)
        visitors[0].update_submit(10)
        comp_visitor.update_submit(10)
        self.assertEqual(comp_visitor.get_stat_data(), "20\n\n10")


if __name__ == "__main__":
    unittest.main()