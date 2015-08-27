import logging

from dao import ContestsDAO, ProblemsDAO
import ejudge_contest
import model
import md5_hasher


def problem_generator(contest_dirs):
    for contest_dir in contest_dirs:
        logging.debug('Entering {}'.format(contest_dir))
        contest = ejudge_contest.EjudgeContest(contest_dir)
        problems_ids = contest.get_problem_ids()
        for problem_id in problems_ids:
            logging.debug('Processing problem {} from contest {}'.format(problem_id[1], contest.contest_id))
            problem_name = contest.get_short_name_by_problem_id(problem_id)
            polygon_id = contest.get_polygon_id_by_problem_id(problem_id)
            tests_paths = contest.get_test_paths_by_problem_id(problem_id)
            tests_hashes = []
            for test_path in tests_paths:
                tests_hashes.append(md5_hasher.get_hash(test_path[0], test_path[1]))
            yield model.Problem(problem_id, polygon_id, problem_name, tests_hashes)


def sqlite_problem_generator(conn):
    cursor = conn.get_cursor()
    cursor.execute('SELECT {} FROM Problems'.format(ProblemsDAO.columns))
    result = cursor.fetchall()

    dao = ProblemsDAO(conn)
    for row in result:
        prob = dao.deep_load(row)
        logging.debug('Processing problem {} from contest {}'.format(prob.problem_id[1], prob.problem_id[0]))
        yield prob


def sqlite_contest_generator(conn):
    cursor = conn.get_cursor()
    cursor.execute('SELECT {} FROM Contests'.format(ContestsDAO.columns))
    result = cursor.fetchall()

    dao = ContestsDAO(conn)
    for row in result:
        cont = dao.deep_load(row)
        logging.debug('Processing contest {}'.format(cont.contest_id))
        yield cont
