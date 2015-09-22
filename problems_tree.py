import logging

SIMILAR_PROBLEMS_MIN_RATIO = 0.5
EPS = 1e-9


class ProblemsTree:
    def __init__(self, problems):
        self.problems = list(problems)
        self.problem_previous = dict()  # problem -> (previous, similarity, same, added, removed)
        for index, problem_1 in enumerate(self.problems):
            if index % 100 == 0 and index > 0:
                logging.info("Build tree: {}/{}".format(index, len(problems)))
            problem_1_tests = set(problem_1.cases)
            for problem_2 in self.problems[index + 1:]:
                problem_2_tests = set(problem_2.cases)
                same_tests_count = len(problem_1_tests & problem_2_tests)
                try:
                    similarity = same_tests_count / max(len(problem_1.cases), len(problem_2.cases))
                except ZeroDivisionError:
                    similarity = 0.0
                if similarity > SIMILAR_PROBLEMS_MIN_RATIO:
                    if problem_2 not in self.problem_previous or \
                                    similarity > self.problem_previous[problem_2][1] - EPS:
                        self.problem_previous[problem_2] = (problem_1, similarity, same_tests_count,
                                                            len(problem_2.cases) - same_tests_count,
                                                            len(problem_1.cases) - same_tests_count)

    def get_problems(self):
        return self.problems

    def get_previous_problem(self, problem):
        if problem in self.problem_previous:
            return self.problem_previous[problem][0]
        else:
            return None

    def get_relation_to_parent(self, problem):
        if problem in self.problem_previous:
            return self.problem_previous[problem]
        else:
            return None

    def __str__(self):
        resulting_string = ''
        for problem in self.problems:
            resulting_string += str(problem) + ': '
            if problem not in self.problem_previous:
                resulting_string += 'it is a new problem. Tests: {tests}.\n'.format(tests=len(set(problem.cases)))
            else:
                previous, similarity, same_tests_count, added_tests_count, removed_tests_count = self.problem_previous[
                    problem]
                if added_tests_count == 0 and removed_tests_count == 0:
                    resulting_string += 'it is {previous}. Tests: {tests}.\n'. \
                        format(previous=str(previous), tests=same_tests_count)
                else:
                    resulting_string += 'is based on {previous}. '.format(previous=str(previous))
                    resulting_string += 'Tests: +{added}, -{removed}, {same} not changed.\n'. \
                        format(added=added_tests_count, removed=removed_tests_count, same=same_tests_count)
        return resulting_string

