import unittest
from multiple_contest_walker import MultipleContestWalker
import os.path


class TestMultiContestWalker(unittest.TestCase):
    def setUp(self):
        self.walker = MultipleContestWalker()

    def test_walk(self):
        contests_dir = os.path.join('testdata', 'ejudge_contest')
        contests = [contest for contest in self.walker.walk(contests_dir)]
        true_contests = [('1', 'testdata\\ejudge_contest\\000001'),
                         ('2', 'testdata\\ejudge_contest\\000002'),
                         ]
        self.assertEqual(sorted(contests), sorted(true_contests))


if __name__ == "__main__":
    unittest.main()
