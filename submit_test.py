import unittest
from submit import Submit
from run import Run

class PositiveTests(unittest.TestCase):
    def setUp(self):
        self.runs = []
        for i in range(2):
            self.runs.append(Run(0, 0, i, 1))
        
    def test_init(self):
        self.submit = Submit(0, 1, 179, self.runs, 1)
        self.assertEqual(self.submit.problem, 1)
        self.assertEqual(self.submit.submit_id, 0)
        self.assertEqual(self.submit.runs, self.runs)
        self.assertEqual(self.submit.user_id, 179)
        self.assertEqual(self.submit.outcome, 1)

    def test_str_runs(self):
        self.submit = Submit(0, 1, 179, self.runs, 1)
        self.assertEqual(str(self.submit), "Submit: 0; Result: 1; User id: 179; Runs: Case #0 Outcome 1, Case #1 Outcome 1.")

    def test_str_0runs(self):   
        self.submit = Submit(0, 1, 179, [], 1)
        self.assertEqual(str(self.submit), "Submit: 0; Result: 1; User id: 179; Runs: .")

if __name__ == "__main__":
    unittest.main() 