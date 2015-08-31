class Submit:
    def __init__(self, submit_id, problem_id, user_id, lang_id, runs, outcome, scoring, timestamp):
        self.problem_id = problem_id
        self.submit_id = submit_id
        self.runs = runs
        self.outcome = outcome
        self.user_id = user_id
        self.lang_id = lang_id
        self.scoring = scoring
        self.timestamp = timestamp
        self.runs_results = ''
        self.count_results()

    def count_results(self):
        self.runs_results = ''.join([str(run.outcome) for run in self.runs])

    def __str__(self):
        return "Submit: {0}; Result: {1}; User id: {2}; Runs: {3}.".format(self.submit_id, self.outcome,
                                                                           self.user_id,
                                                                           ", ".join([str(run)
                                                                                      for run in self.runs]))


class Run:
    def __init__(self, problem_id, submit_id, case_id, real_time, time, outcome):
        self.problem_id = problem_id
        self.submit_id = submit_id
        self.case_id = case_id
        self.real_time = real_time
        self.time = time
        self.outcome = outcome

    def __str__(self):
        result = "Case #{0} Outcome {1}".format(str(self.case_id), str(self.outcome))
        return result

    def __repr__(self):
        return str(self)


class Problem:
    def __init__(self, problem_id, polygon_id, name, cases):
        self.problem_id = problem_id
        self.polygon_id = polygon_id or ''
        self.name = name
        self.cases = cases

    def __str__(self):
        return 'Problem #{0} ("{1}") from contest #{2}'.format(self.problem_id[1], self.name, self.problem_id[0])


class User:
    def __init__(self, user_id, origin):
        self.user_id = user_id
        self.origin = origin

    def __str__(self):
        return 'User #{} from {}'.format(self.user_id, self.origin)


class Contest:
    def __init__(self, contest_id, origin, name, scoring):
        self.contest_id = contest_id
        self.origin = origin
        self.name = name
        self.scoring = scoring

    def __str__(self):
        return 'Contest {} (#{}) from {}, scoring {}'.format(self.name, self.contest_id, self.origin, self.scoring)

