import logging

from db_submits_filler import DBSubmitsFiller

from ejudge_database import EjudgeDatabase
from walker import SubmitWalker, MultipleContestWalker, EjudgeRunsFilesWorker


def create_submit_walker(cursor=None):
    if cursor:
        return SubmitWalker(EjudgeDatabase(cursor))
    return SubmitWalker(None)


def fill_from_xml(sqlite_cursor, ejudge_cursor, start_dir, origin):
    walker = create_submit_walker(ejudge_cursor)
    filler = DBSubmitsFiller(sqlite_cursor)
    for contest_id, contest_dir in MultipleContestWalker().walk(start_dir):
        logging.info("Filling contest #{0}".format(contest_id))
        walker.contest_id = contest_id
        processed_submits = 0
        for filename in EjudgeRunsFilesWorker().walk(contest_dir):
            for submit in walker.walk(filename[1]):
                if submit is not None:
                    filler.fill_db_from_submit(submit, origin)
                    processed_submits += 1
                    if processed_submits % 100 == 0:
                        logging.info('Filled in {0} submits from contest #{1}'.format(processed_submits,
                                                                                      contest_id))
                else:
                    logging.debug('{} is broken, skipping'.format(filename[1]))
        logging.info('Contest #{0} was finished, filled in {1} submits'.format(contest_id,
                                                                               processed_submits))
