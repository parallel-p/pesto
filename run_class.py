class Run:
	def __init__(self, problem, submit_id, case_id, outcome):
		self.problem = problem
		self.submit_id = submit_id
		self.case_id = case_id
		self.outcome = outcome

	def __str__(self):
		_result = "Case #" + str(self.case_id) + " Outcome " + str(self.outcome)
		return _result


def main(): # testing print and Run.__str__()
	n = int(input())
	runs = []
	for i in range(n):
		single_run = [int(i) for i in input().split()]
		runs.append(Run(*single_run))
	for i in range(len(runs)):
		print(runs[i])


if __name__ == "__main__": 
	main()