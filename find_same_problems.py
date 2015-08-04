def find_same_problems(problem_list):
    cases_to_problems = dict()
    for problem in problem_list:
        key = tuple(problem.cases)
        if key not in cases_to_problems:
            cases_to_problems[key] = [problem]
        else:
            cases_to_problems[key].append(problem)

    result = []
    for problems in cases_to_problems.values():
        if len(problems) > 1:
            result.append(sorted(problems, key=lambda x: x.problem_id))

    result.sort(key=lambda x: x[0].problem_id)
    return result
