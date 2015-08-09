from db_submits_filler import DBSubmitsFiller
from ejudge_database import EjudgeDatabase


from walker import PickleWorker, SubmitWalker, MultipleContestWalker, EjudgeRunsFilesWorker


def create_submit_walker(cursor=None):
    if cursor:
        return SubmitWalker(EjudgeDatabase(cursor))
    return SubmitWalker(None)


def fill_from_pickles(sqlite_cursor, pickle_dir, origin):
    walker = create_submit_walker()
    pw = PickleWorker()
    filler = DBSubmitsFiller(sqlite_cursor)
    for filename in pw.walk(pickle_dir):
        for submit in walker.walk(filename[1]):
            if submit is not None:
                filler.fill_db_from_submit(submit, origin)


def fill_from_xml(sqlite_cursor, ejudge_cursor, start_dir, origin):
    walker = create_submit_walker(ejudge_cursor)
    filler = DBSubmitsFiller(sqlite_cursor)
    for contest_id, contest_dir in MultipleContestWalker().walk(start_dir):
        walker.contest_id = contest_id
        for filename in EjudgeRunsFilesWorker().walk(contest_dir):
            for submit in walker.walk(filename[1]):
                if submit is not None:
                    filler.fill_db_from_submit(submit, origin)
