class Problem:

    def __init__(self, contest_id, problem_id, case_ids):
        """
        :type contest_id: str or int
        :type problem_id: str or int
        :type case_ids: list
        """
        self.contest_id = contest_id
        self.problem_id = problem_id
        self.case_ids = case_ids

    def __str__(self):
        return 'Contest #{0} Problem #{1}\nCases: {2}'.format(self.contest_id,
                                                              self.problem_id,
                                                              self.case_ids)
    def get_submits(self, database): #Returns all submits for particular problem
        result = list()
        for submit in database.submits:
            if submit.problem.problem_id == self.problem_id:
                result.append(submit)
        return result
