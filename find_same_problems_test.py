import unittest
from unittest.mock import Mock
from find_same_problems import find_same_problems


class TestFindSameProblems(unittest.TestCase):
    def test_common(self):
        problems = []
        problems.append(Mock(cases=['1', '2', '3'], problem_id=('17', '1')))
        problems.append(Mock(cases=['4', '5', '6'], problem_id=('17', '2')))
        problems.append(Mock(cases=['1', '2', '3'], problem_id=('17', '3')))
        problems.append(Mock(cases=['1', '2', '3'], problem_id=('18', '1')))
        problems.append(Mock(cases=['4', '5', '6'], problem_id=('18', '2')))
        problems.append(Mock(cases=['7', '8', '9'], problem_id=('18', '3')))
        result = find_same_problems(problems)
        self.assertEqual(len(result), 2)
        problems = [p.problem_id for p in result[0]]
        self.assertEqual(problems, [('17', '1'), ('17', '3'), ('18', '1')])
        problems = [p.problem_id for p in result[1]]
        self.assertEqual(problems, [('17', '2'), ('18', '2')])

if __name__ == "__main__":
    unittest.main()
