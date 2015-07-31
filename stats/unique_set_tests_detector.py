

def get_uniq_test_results(base_dir, database_filename):
    database = MemoryDatabase(base_dir, database_filename)
    problems = dict()
    problems_id = []

    for problem in database.problems.values():
        problems[problem.problem_id] = dict()
        problems_id.append(problem.problem_id)
    runs_by_runs_result = dict()
    for submit in database.submits:
        problem_id = submit.problem.problem_id
        runs_results = submit.runs_results

        if runs_results in problems[problem_id]:
            problems[problem_id][runs_results] += 1
        else:
            problems[problem_id][runs_results] = 1
            runs_by_runs_result[runs_results] = submit.runs

    uniq_test_results = []

    for problem_id in problems_id:
        uniq_test_results.append([])
        for runs_result in problems[problem_id]:
            uniq_test_results[-1].append([runs_by_runs_result[runs_result], problems[problem_id][runs_result]])

    return uniq_test_results


if __name__ == '__main__':
    print('Enter contests base dir name:')
    base_dir = input()
    print('Enter database filename:')
    database_filename = input()

    uniq_test_res = get_uniq_test_results(base_dir, database_filename)

    for problem_id, uniq_results in enumerate(uniq_test_res):
        print("Problem", problem_id)
        print("Uniq test resuls:")

        for result in uniq_results:
            print('    Testing result:{0}, Submits count:{1}'.format(' '.join([el.outcome for el in result[0]]), result[1]), sep="\n")