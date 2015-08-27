import unittest
from unittest.mock import Mock

from find_same_problems import SameProblemsFinder


class TestFindSameProblems(unittest.TestCase):
    def setUp(self):
        problems = []
        problems.append(Mock(cases=['1', '2', '3'], problem_id=('17', '1')))
        problems[-1].name = 'A'  # Mock(name='A') will not work as you expecting!
        problems.append(Mock(cases=['4', '5', '6'], problem_id=('17', '2')))
        problems[-1].name = 'B'
        problems.append(Mock(cases=['1', '2', '3'], problem_id=('17', '3')))
        problems[-1].name = 'C'
        problems.append(Mock(cases=['1', '2', '3'], problem_id=('18', '1')))
        problems[-1].name = 'D'
        problems.append(Mock(cases=['4', '5', '6'], problem_id=('18', '2')))
        problems[-1].name = 'E'
        problems.append(Mock(cases=['7', '8', '9'], problem_id=('18', '3')))
        problems[-1].name = '1337'
        self.finder = SameProblemsFinder(problems)

    def test_common(self):
        result = self.finder.get_stat_data()
        self.assertEqual(len(result), 2)
        problems = [p.problem_id for p in result[0]]
        self.assertEqual(problems, [('17', '1'), ('17', '3'), ('18', '1')])
        problems = [p.problem_id for p in result[1]]
        self.assertEqual(problems, [('17', '2'), ('18', '2')])

    def test_str(self):
        result = str(self.finder)
        self.assertEqual(result,
                         'Problems "A" from contest 17, "C" from contest 17, "D" from contest 18 are same.\nProblems "B" from contest 17, "E" from contest 18 are same.\n')


if __name__ == "__main__":
    unittest.main()
