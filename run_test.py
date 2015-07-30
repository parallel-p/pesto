import unittest
from run import Run


class TestRun(unittest.TestCase):
    
    def setUp(self):
        self.run = Run(None, '1', '2', 'OK')

    def test_init(self):
        self.assertEqual(self.run.problem, None)
        self.assertEqual(self.run.submit_id, '1')
        self.assertEqual(self.run.case_id, '2')
        self.assertEqual(self.run.outcome, 'OK')

    def test_str(self):
        self.assertEqual(str(self.run), "Case #2 Outcome OK")

if __name__ == '__main__':
    unittest.main()