from problem_generator import problem_generator


def extract_cases_to_db(contest_dirs, cursor, origin):
    problems = problem_generator(contest_dirs)
    contests_len = cursor.execute('SELECT COUNT(id) FROM Contests').fetchone()[0]
    if contests_len == 0:
        return
    for problem in problems:
        contest_ref = cursor.execute('SELECT id FROM Contests WHERE origin = ? AND contest_id = ?',\
                                    (origin, problem.problem_id[0])).fetchone()[0]
        cursor.execute('UPDATE Problems SET name = ? WHERE contest_ref = ? AND problem_id = ?',\
                                    (problem.name, contest_ref, problem.problem_id[1]))
        problem_ref = cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',\
                                    (contest_ref, problem.problem_id[1])).fetchone()[0]
        for case_num in range(len(problem.cases)):
            cursor.execute('UPDATE Cases SET io_hash = ? WHERE problem_ref = ? AND case_id = ?',\
                            (problem.cases[case_num], problem_ref, case_num + 1))