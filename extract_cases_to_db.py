from problem_generator import problem_generator


def extract_cases_to_db(contest_dirs, cursor, origin):
    problems = problem_generator(contest_dirs)
    contests_len = cursor.execute('SELECT COUNT(id) FROM Contests').fetchone()
    if contests_len is None or contests_len[0] == 0:
        print('Database is empty')
        return

    for problem in problems:
        contest_response = cursor.execute('SELECT id FROM Contests WHERE origin = ? AND contest_id = ?',
                                    (origin, problem.problem_id[0].rjust(6, '0'))).fetchone()
        if contest_response is None:
            continue

        contest_ref = contest_response[0]
        cursor.execute('UPDATE Problems SET name = ? WHERE contest_ref = ? AND problem_id = ?',
                                    (problem.name, contest_ref, problem.problem_id[1]))
        problem_response = cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                                    (contest_ref, problem.problem_id[1])).fetchone()
        if problem_response is None:
            continue

        problem_ref = problem_response[0]
        for case_num in range(len(problem.cases)):
            cursor.execute('UPDATE Cases SET io_hash = ? WHERE problem_ref = ? AND case_id = ?',
                            (problem.cases[case_num], problem_ref, case_num + 1))