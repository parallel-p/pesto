import unittest
from visitor_factory import VisitorFactory
from visitor import Visitor


class VisitorFactoryTest(unittest.TestCase):
    def test_keys(self):
        VisitorFactory.create(None)
        VisitorFactory.create(0)
        VisitorFactory.create('-')
        VisitorFactory.create([1, 2])
        VisitorFactory.create((1, 2))
        VisitorFactory.create({1: 2})
    
    def test_result(self):
        self.assertTrue(isinstance(VisitorFactory.create(0), Visitor))
