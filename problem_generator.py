import ejudge_contest
import model
import md5_hasher
import sqlite_connector
from dao_problems import DAOProblems


def problem_generator(contest_dirs):
    for contest_dir in contest_dirs:
        contest = ejudge_contest.EjudgeContest(contest_dir)
        contest_id = contest.get_contest_id()
        problems_ids = contest.get_problem_ids()
        for problem_id in problems_ids:
            problem_name = contest.get_short_name_by_problem_id(problem_id)
            tests_paths = contest.get_test_paths_by_problem_id(problem_id)
            tests_hashes = []
            for test_path in tests_paths:
                tests_hashes.append(md5_hasher.get_hash(test_path[0], test_path[1]))
            yield model.Problem(problem_id, problem_name, tests_hashes)

def connect(conn, file):
    conn.create_connection(file)
    cursor = conn.get_cursor()
    return cursor

def sqlite_problem_generator(sqlite_filename):
    conn = sqlite_connector.SQLiteConnector()
    cursor = connect(conn, sqlite_filename)
    cursor.execute('SELECT {} FROM Problems'.format(DAOProblems.columns))
    result = cursor.fetchall()

    dao = DAOProblems(conn)
    for row in result:
        yield dao.deep_load(row)
