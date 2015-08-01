import unittest
from visitor import FakeVisitor
from compositor_visitor import CompositorVisitor
from visitor_factory import VisitorFactory
from composite_factory import CompositeVisitorFactory

class FakeFactory(VisitorFactory):
    @staticmethod
    def create(key):
        return FakeVisitor()


class FunctionTesting(unittest.TestCase):
    def test_empty_output(self):
        comp_visitor = CompositorVisitor()
        self.assertEqual(CompositeVisitorFactory.create(0).get_stat_data(), comp_visitor.get_stat_data())

    def test_one_visitor_factory(self):
        visitor = FakeVisitor()
        comp_visitor = CompositorVisitor(visitor)
        self.assertEqual(CompositeVisitorFactory.create(0, FakeFactory).pretty_print(), comp_visitor.pretty_print())

    def test_two_visitor_factories(self):
        visitors = []
        factories = []
        for i in range(2):
            visitors.append(FakeVisitor())
            factories.append(FakeFactory)
        comp_visitor = CompositorVisitor(*visitors)
        self.assertEqual(CompositeVisitorFactory.create(0, *factories).get_stat_data(), comp_visitor.get_stat_data())


if __name__ == "__main__":
    unittest.main()
