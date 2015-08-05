similar_problems_min_ratio = 0.749999


def find_similar_problems(problem_list):
    result = []
    for i in range(len(problem_list)):
        problem_1 = problem_list[i]
        problem_1_tests = set(problem_1.cases)
        for problem_2 in problem_list[i+1:]:
            same_tests_count = 0
            for problem_2_test in problem_2.cases:
                if problem_2_test in problem_1_tests:
                    same_tests_count += 1
            if same_tests_count > similar_problems_min_ratio * min(len(problem_1.cases), len(problem_2.cases)):
                result.append((problem_1.problem_id, problem_2.problem_id))
    return result

