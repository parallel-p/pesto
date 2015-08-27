SIMILAR_PROBLEMS_MIN_RATIO = 0.5


class SimilarProblemsFinder:
    def __init__(self, problems):
        self.same_tests_count_dict = dict()
        self.similarity_dict = dict()
        problem_list = list(problems)
        self.result = []
        for i in range(len(problem_list)):
            problem_1 = problem_list[i]
            problem_1_tests = set(problem_1.cases)
            for problem_2 in problem_list[i + 1:]:
                same_tests_count = 0
                for problem_2_test in problem_2.cases:
                    if problem_2_test in problem_1_tests:
                        same_tests_count += 1
                try:
                    similarity = same_tests_count / max(len(problem_1.cases), len(problem_2.cases))
                except ZeroDivisionError:
                    similarity = 0.0
                if similarity > SIMILAR_PROBLEMS_MIN_RATIO:
                    self.result.append((problem_1, problem_2))
                self.same_tests_count_dict[(problem_1, problem_2)] = same_tests_count
                self.similarity_dict[(problem_1, problem_2)] = similarity
                self.same_tests_count_dict[(problem_2, problem_1)] = same_tests_count
                self.similarity_dict[(problem_2, problem_1)] = similarity

    def get_stat_data(self):
        return self.result

    def get_same_tests_count(self, problem_1, problem_2):
        return self.same_tests_count_dict[(problem_1, problem_2)]

    def get_added_tests_count(self, problem_1, problem_2):
        return len(problem_2.cases) - self.same_tests_count_dict[(problem_1, problem_2)]

    def get_removed_tests_count(self, problem_1, problem_2):
        return len(problem_1.cases) - self.same_tests_count_dict[(problem_1, problem_2)]

    def get_similarity(self, problem_1, problem_2):
        return self.similarity_dict[(problem_1, problem_2)]

    def __str__(self):
        resulting_string = ''
        template = 'Problems {p1} from contest #{c1} and problem {p2} from contest #{c2} are similar ({similarity}%).'
        template += ' Tests: +{added}, -{removed}, {same} not changed.\n'
        for pair in self.result:
            added_tests_count = self.get_added_tests_count(pair[0], pair[1])
            removed_tests_count = self.get_removed_tests_count(pair[0], pair[1])
            same_tests_count = self.get_same_tests_count(pair[0], pair[1])
            resulting_string += template.format(p1=pair[0].name, c1=pair[0].problem_id[0],
                                                p2=pair[1].name, c2=pair[1].problem_id[0],
                                                similarity=int(self.get_similarity(pair[0], pair[1]) * 100),
                                                added=added_tests_count, removed=removed_tests_count,
                                                same=same_tests_count)
        return resulting_string
