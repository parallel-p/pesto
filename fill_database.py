from fill_db_from_submit import fill_db_from_submit
from ejudge_database import EjudgeDatabase


from walker import PickleWorker, SubmitWalker, MultipleContestWalker, EjudgeRunsFilesWorker


def create_submit_walker(cursor):
    return SubmitWalker(EjudgeDatabase(cursor))


def fill_from_pickles(sqlite_cursor, ejudge_cursor, pickle_dir, origin):
    walker = create_submit_walker(ejudge_cursor)
    pw = PickleWorker()
    for filename in pw.walk(pickle_dir):
        for submit in walker.walk(filename[1]):
            fill_db_from_submit(sqlite_cursor, submit, origin)


def fill_from_xml(sqlite_cursor, ejudge_cursor, start_dir, origin):
    walker = create_submit_walker(ejudge_cursor)
    for contest_id, contest_dir in MultipleContestWalker().walk(start_dir):
        walker.contest_id = contest_id
        for filename in EjudgeRunsFilesWorker().walk(contest_dir):
            for submit in walker.walk(filename[1]):
                fill_db_from_submit(sqlite_cursor, submit, origin)
