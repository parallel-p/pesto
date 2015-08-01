import unittest
from visitor_factory import VisitorFactory
from visitor import Visitor


class VisitorFactoryTest(unittest.TestCase):
    def test_keys(self):
        factory = VisitorFactory()
        factory.create(None)
        factory.create(0)
        factory.create('-')
        factory.create([1, 2])
        factory.create((1, 2))
        factory.create({1: 2})
    
    def test_result(self):
        factory = VisitorFactory()
        self.assertTrue(isinstance(factory.create(0), Visitor))
