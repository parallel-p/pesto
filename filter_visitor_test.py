import unittest
from unittest.mock import Mock
import filter_visitor


class TestFilterVisitor(unittest.TestCase):
    def test_init(self):
        filter = filter_visitor.FilterVisitor(1, '2')
        self.assertEqual(filter.key, '2')
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


class TestFilterAllCasesTestedSubmits(unittest.TestCase):
    def setUp(self):
        self.good_submit = Mock(problem_id=('17', '1'), runs=['1'])
        self.bad_submit = Mock(problem_id=('17', '2'), runs = ['1'])
        self.key = {('17', '1'): 1, ('17', '2'): 2}
        self.visitor = Mock()
        self.visitor.visit = Mock()
        self.filter = filter_visitor.FilterAllCasesTestedSubmits(self.visitor, self.key)

    def test_good_submit(self):
        self.filter.visit(self.good_submit)
        self.visitor.visit.assert_called_once_with(self.good_submit)

    def test_bad_submit(self):
        self.filter.visit(self.bad_submit)
        self.assertTrue(len(self.visitor.visit.mock_calls) == 0)


class TestFilterByScoringSystem(unittest.TestCase):
	def setUp(self):
		self.good_submit = Mock(scoring='acm')
		self.good_submit_upper = Mock(scoring='ACM')
		self.good_submit_mixed = Mock(scoring='Acm')
		self.bad_submit = Mock(scoring='kirov')
		self.visitor = Mock()
		self.visitor.visit = Mock()

	def test_good_submit(self):
		filter_lower = filter_visitor.FilterByScoringSystem(self.visitor, 'acm')
		filter_upper = filter_visitor.FilterByScoringSystem(self.visitor, 'ACM')
		filter_mixed = filter_visitor.FilterByScoringSystem(self.visitor, 'Acm')

		filter_lower.visit(self.good_submit)
		filter_lower.visit(self.good_submit_upper)
		filter_lower.visit(self.good_submit_mixed)
		self.assertTrue(len(self.visitor.visit.mock_calls) == 3)
		self.visitor.visit.mock_calls = []

		filter_upper.visit(self.good_submit)
		filter_upper.visit(self.good_submit_upper)
		filter_upper.visit(self.good_submit_mixed)
		self.assertTrue(len(self.visitor.visit.mock_calls) == 3)
		self.visitor.visit.mock_calls = []

		filter_mixed.visit(self.good_submit)
		filter_mixed.visit(self.good_submit_upper)
		filter_mixed.visit(self.good_submit_mixed)
		self.assertTrue(len(self.visitor.visit.mock_calls) == 3)

	def test_bad_submit(self):
		self.filter = filter_visitor.FilterByScoringSystem(self.visitor, 'acm')
		self.filter.visit(self.bad_submit)
		self.assertTrue(len(self.visitor.visit.mock_calls) == 0)

if __name__ == "main":
    unittest.main()
