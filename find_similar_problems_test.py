import unittest
from unittest.mock import Mock
from find_similar_problems import SimilarProblemsFinder


class TestFindSameProblems(unittest.TestCase):
    def setUp(self):
        self.problems = []
        self.problems.append(Mock(cases=['a1', 'a2', 'a3', 'a4', 'a5', 'a6'], problem_id=('42', '1')))
        self.problems[-1].name = '42a'
        self.problems.append(Mock(cases=['b1', 'b2', 'b3', 'b4', 'b5'], problem_id=('42', '2')))
        self.problems[-1].name = '42b'
        self.problems.append(Mock(cases=['a1', 'a2', 'a3', 'a4', 'a5', 'a7'], problem_id=('43', '1')))
        self.problems[-1].name = '43a'
        self.problems.append(Mock(cases=['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7'], problem_id=('43', '2')))
        self.problems[-1].name = '43b'
        self.finder = SimilarProblemsFinder(self.problems)

    def test_common(self):
        result = self.finder.get_similar_problems_pairs()
        self.assertEqual(len(result), 2)
        self.assertTrue((self.problems[0], self.problems[2]) in result)
        self.assertTrue((self.problems[1], self.problems[3]) in result)

    def test_str(self):
        result_string = str(self.finder)
        correct_string = """Problems 42a from contest #42 and problem 43a from contest #43 are similar.
Problems 42b from contest #42 and problem 43b from contest #43 are similar.
"""
        self.assertEqual(sorted(result_string.split('\n')), sorted(correct_string.split('\n')))


if __name__ == "__main__":
    unittest.main()

