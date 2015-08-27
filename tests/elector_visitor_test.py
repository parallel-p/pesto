import unittest
from unittest.mock import Mock

from elector_visitor import ElectorVisitor
from elector_visitor import ElectorByMaxCasesVisitor


class TestElectorVisitor(unittest.TestCase):
    def setUp(self):
        self.elector = ElectorVisitor(228)

    def test_init(self):
        self.assertEqual(self.elector.factory, 228)
        self.assertIsNone(self.elector.key)
        self.assertIsNone(self.elector.visitor)

    def test_submits(self):
        factory, visitor1, visitor2 = Mock(), Mock(), Mock()
        visitor1.submits, visitor2.submits = list(), list()
        visitor1.visit = lambda submit: visitor1.submits.append(submit)
        visitor2.visit = lambda submit: visitor2.submits.append(submit)
        self.elector.factory = factory
        factory.create.return_value = visitor1
        self.elector.visit('15')
        self.assertEqual(self.elector.key, '15')
        self.assertEqual(self.elector.visitor, visitor1)
        self.assertEqual(visitor1.submits, ['15'])
        factory.create.return_value = visitor2
        self.elector.visit('21')
        self.assertEqual(self.elector.key, '21')
        self.assertEqual(self.elector.visitor, visitor2)
        self.assertEqual(visitor2.submits, ['21'])
        self.elector.visit('21')
        self.assertEqual(self.elector.key, '21')
        self.assertEqual(self.elector.visitor, visitor2)
        self.assertEqual(visitor2.submits, ['21', '21'])

    def test_non_visitor_print(self):
        self.assertEqual(self.elector.pretty_print(), '')

    def test_key_comparator(self):
        self.elector.key = 25
        self.assertTrue(self.elector.is_key_better(26))
        self.assertFalse(self.elector.is_key_better(24))

    def test_non_key_comparator(self):
        self.assertTrue(self.elector.is_key_better(5))

    def test_print(self):
        visitor = Mock()
        visitor.pretty_print.return_value = 'kek'
        self.elector.visitor = visitor
        self.assertEqual(self.elector.pretty_print(), 'kek')

    def test_key(self):
        self.assertEqual(self.elector.build_key(125), '125')

    def test_stat_data(self):
        self.assertFalse(self.elector.get_stat_data())
        self.elector.visitor = Mock(get_stat_data=Mock(return_value=42))
        self.assertEqual(self.elector.get_stat_data(), 42)


class TestElectorByMaxCases(unittest.TestCase):
    def test_key(self):
        elector = ElectorByMaxCasesVisitor(None)
        submit = Mock()
        submit.runs = [1, 2, 3]
        self.assertEqual(elector.build_key(submit), 3)


if __name__ == "__main__":
    unittest.main()
