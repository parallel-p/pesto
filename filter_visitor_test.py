import unittest
from unittest.mock import Mock
import filter_visitor



class TestFilterVisitor(unittest.TestCase):
    def test_init(self):
        filter = filter_visitor.FilterVisitor(1, 2)
        self.assertEqual(filter.key, 2)
        self.assertEqual(filter.next_visitor, 1)

    def test_get_stat_data(self):
        visitor = Mock()
        visitor.get_stat_data = Mock(return_value="mock_info")
        filter = filter_visitor.FilterVisitor(visitor, 2)
        stat = filter.get_stat_data()
        self.assertEqual(stat, 'mock_info')

class TestFilterByContestVisitor(unittest.TestCase):
    def setUp(self):
        self.good_submit = Mock(problem_id=("17", "12"))
        self.bad_submit = Mock(problem_id=("71", "21"))

        self.visitor = Mock()

        self.filter = filter_visitor.FilterByContestVisitor(self.visitor, "17")

    def test_good_submit(self):
        self.filter.visit(self.good_submit)
        self.visitor.visit.assert_called_once_with(self.good_submit)

    def test_bad_submit(self):
        self.filter.visit(self.bad_submit)
        self.assertTrue(len(self.visitor.visit.mock_calls) == 0)


class TestFilterByProblemVisitor(unittest.TestCase):
    def setUp(self):
        self.good_submit = Mock(problem_id=("17", "12"))
        self.bad_submit = Mock(problem_id=("71", "21"))

        self.visitor = Mock()
        self.filter = filter_visitor.FilterByProblemVisitor(self.visitor, "12")

    def test_good_submit(self):
        self.filter.visit(self.good_submit)
        self.visitor.visit.assert_called_once_with(self.good_submit)

    def test_bad_submit(self):
        self.filter.visit(self.bad_submit)
        self.assertTrue(len(self.visitor.visit.mock_calls) == 0)

class TestFilterByUserVisitor(unittest.TestCase):
    def setUp(self):
        self.good_submit = Mock(user_id="good_gay")
        self.bad_submit = Mock(user_id="bad_gay")

        self.visitor = Mock()
        self.filter = filter_visitor.FilterByUserVisitor(self.visitor, "good_gay")

    def test_good_submit(self):
        self.filter.visit(self.good_submit)
        self.visitor.visit.assert_called_once_with(self.good_submit)

    def test_bad_submit(self):
        self.filter.visit(self.bad_submit)
        self.assertTrue(len(self.visitor.visit.mock_calls) == 0)


if __name__ == "main":
    unittest.main()