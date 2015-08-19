import ejudge_contest
import model
import md5_hasher
import sqlite_connector
from dao_problems import DAOProblems
from dao_contests import DAOContests


def problem_generator(contest_dirs):
    for contest_dir in contest_dirs:
        contest = ejudge_contest.EjudgeContest(contest_dir)
        problems_ids = contest.get_problem_ids()
        for problem_id in problems_ids:
            problem_name = contest.get_short_name_by_problem_id(problem_id)
            tests_paths = contest.get_test_paths_by_problem_id(problem_id)
            tests_hashes = []
            for test_path in tests_paths:
                tests_hashes.append(md5_hasher.get_hash(test_path[0], test_path[1]))
            yield model.Problem(problem_id, problem_name, tests_hashes)


def sqlite_problem_generator(conn):
    cursor = conn.get_cursor()
    cursor.execute('SELECT {} FROM Problems'.format(DAOProblems.columns))
    result = cursor.fetchall()

    dao = DAOProblems(conn)
    for row in result:
        yield dao.deep_load(row)


def sqlite_contest_generator(conn):
    cursor = conn.get_cursor()
    cursor.execute('SELECT {} FROM Contests'.format(DAOContests.columns))
    result = cursor.fetchall()

    dao = DAOContests(conn)
    for row in result:
        yield dao.deep_load(row)
