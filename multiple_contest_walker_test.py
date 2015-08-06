import unittest
from multiple_contest_walker import MultipleContestWalker
import os.path


class TestMultiContestWalker(unittest.TestCase):
    def setUp(self):
        contests_dir = os.path.join('testdata', 'ejudge_contest')
        self.walker = MultipleContestWalker()
        self.contests = [contest for contest in self.walker.walk(contests_dir)]
        self.true_contests = [('1', os.path.join('testdata', 'ejudge_contest', '000001')),
                         ('2', os.path.join('testdata', 'ejudge_contest', '000002'))]

    def test_walk(self):
        self.assertEqual(sorted(self.contests), sorted(self.true_contests))

    def test_non_digit_folder(self):
        self.assertFalse(('definitely_not_a_contest',
                          os.path.join('testdata',
                                       'ejudge_contest',
                                       'definitely_not_a_contest')) in self.contests)

    def test_non_6_chars_folder(self):
        self.assertFalse(('420', os.path.join('testdata', 'ejudge_contest', '420')) in
                         self.contests)


if __name__ == "__main__":
    unittest.main()
