import unittest
from visitor_factory import VisitorFactory
from visitor import Visitor


class VisitorFactoryTest(unittest.TestCase):
    def test_result(self):
        factory = VisitorFactory()
        self.assertTrue(isinstance(factory.create(0), Visitor))
