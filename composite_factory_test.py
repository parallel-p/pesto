import unittest
from visitor import FakeVisitor
from compositor_visitor import CompositorVisitor
from visitor_factory import VisitorFactory
from composite_factory import CompositeVisitorFactory

class FakeFactory(VisitorFactory):
    def create(self, key):
        return FakeVisitor()

class FunctionTesting(unittest.TestCase):
    def test_type_of_return(self):
        comp_visitor = CompositorVisitor()
        comp_factory = CompositeVisitorFactory()
        self.assertEqual(comp_factory.create(0).__class__, comp_visitor.__class__)

    def test_containing_factories(self):
        factory = FakeFactory()
        comp_factory = CompositeVisitorFactory(FakeFactory())
        self.assertEqual(comp_factory.factories[0].__class__, factory.__class__)

    def test_two_visitor(self):
        visitors = []
        factories = []
        for i in range(2):
            visitors.append(FakeVisitor())
            factories.append(FakeFactory())

        comp_visitor = CompositorVisitor(*visitors)
        comp_factory = CompositeVisitorFactory(*factories)
        self.assertEqual(comp_factory.create(0).get_stat_data(), comp_visitor.get_stat_data())


if __name__ == "__main__":
    unittest.main()
