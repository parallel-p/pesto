similar_problems_min_ratio = 0.749999


class SimilarProblemsFinder:
    def __init__(self, problem_list):
        self.result = []
        for i in range(len(problem_list)):
            problem_1 = problem_list[i]
            problem_1_tests = set(problem_1.cases)
            for problem_2 in problem_list[i+1:]:
                same_tests_count = 0
                for problem_2_test in problem_2.cases:
                    if problem_2_test in problem_1_tests:
                        same_tests_count += 1
                if same_tests_count > similar_problems_min_ratio * min(len(problem_1.cases), len(problem_2.cases)):
                    self.result.append((problem_1, problem_2))

    def get_similar_problems_pairs(self):
        return self.result

    def __str__(self):
        resulting_string = ''
        template = 'Problems {p1} from contest #{c1} and problem {p2} from contest #{c2} are similar.\n'
        for pair in self.result:
            resulting_string += template.format(p1=pair[0].name, c1=pair[0].problem_id[0],
                                                p2=pair[1].name, c2=pair[1].problem_id[0])
        return resulting_string
