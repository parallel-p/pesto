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
        problem_in_db = len(cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                                        (contest_ref, problem.problem_id[1])).fetchall())
        if problem_in_db:
            cursor.execute('UPDATE Problems SET name = ? WHERE contest_ref = ? AND problem_id = ?',
                                        (problem.name, contest_ref, problem.problem_id[1]))
        else:
            cursor.execute('INSERT INTO Problems (id, contest_ref, problem_id, name) VALUES (NULL, ?, ?, ?)',
                           (contest_ref, problem.problem_id[1], problem.name))
        problem_response = cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                                    (contest_ref, problem.problem_id[1])).fetchone()
        if problem_response is None:
            continue

        problem_ref = problem_response[0]

        for case_num in range(len(problem.cases)):
            cursor.execute('UPDATE Cases SET io_hash = ? WHERE problem_ref = ? AND case_id = ?',
                            (problem.cases[case_num], problem_ref, case_num + 1))
            if case_num % 50 == 0 and case_num != 0:
                print('Filled in {0} cases of problem # {1} from contest #{2}'.format(case_num,
                                                                                      problem.problem_id[1],
                                                                                      problem.problem_id[0]))

        print('Filled in {0} cases of problem # {1} from contest #{2}'.format(case_num,
                                                                              problem.problem_id[1],
                                                                              problem.problem_id[0]))