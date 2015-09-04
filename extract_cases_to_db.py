import logging

from problem_generator import problem_generator


def extract_cases_to_db(contest_dirs, cursor, origin, start_from='1'):
    problems = problem_generator(contest_dirs)
    contests_len = cursor.execute('SELECT COUNT(id) FROM Contests').fetchone()
    if contests_len is None or contests_len[0] == 0:
        logging.info('Database is empty')
        return

    for problem in problems:
        if problem.problem_id[0].rjust(6, '0') < start_from.rjust(6, '0'):
            continue

        logging.info('Filling in cases for problem #{0} from contest #{1}'.format(problem.problem_id[1],
                                                                                  problem.problem_id[0]))
        contest_response = cursor.execute('SELECT id FROM Contests WHERE origin = ? AND contest_id = ?',
                                          (origin, problem.problem_id[0].rjust(6, '0'))).fetchone()
        if contest_response is None:
            logging.warning('Contest #{} not found'.format(problem.problem_id[0]))
            continue

        for contest_ref in contest_response:
            problem_in_db = len(cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                                               (contest_ref, problem.problem_id[1])).fetchall())
            if problem_in_db:
                cursor.execute('UPDATE Problems SET name = ?, polygon_id = ? WHERE contest_ref = ? AND problem_id = ?',
                               (problem.name, problem.polygon_id, contest_ref, problem.problem_id[1]))
            else:
                cursor.execute('INSERT INTO Problems (id, contest_ref, polygon_id, problem_id, name) VALUES (NULL, ?, ?, ?, ?)',
                               (contest_ref, problem.polygon_id, problem.problem_id[1], problem.name))
            problem_response = cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                                              (contest_ref, problem.problem_id[1])).fetchone()
            if problem_response is None:
                logging.warning('Problem {} not found'.format(problem.problem_id))
                continue

            for problem_ref in problem_response:
                for case_num in range(len(problem.cases)):
                    cursor.execute('UPDATE Cases SET io_hash = ? WHERE problem_ref = ? AND case_id = ?',
                                   (problem.cases[case_num], problem_ref, case_num + 1))
                    if case_num % 50 == 0 and case_num != 0:
                        logging.info('Filled in {0} cases of problem # {1} from contest #{2}'.format(case_num,
                                                                                                     problem.problem_id[
                                                                                                         1],
                                                                                                     problem.problem_id[
                                                                                                         0]))

                logging.info('Filled in {0} cases of problem #{1} from contest #{2}'.format(case_num,
                                                                                            problem.problem_id[1],
                                                                                            problem.problem_id[0]))
