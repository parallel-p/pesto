import os
import logging

from ejudge_contest_xml import ejudge_get_contest_name
from walker import AllFilesWalker


def fill_db_from_contest_xml(contest_xmls_dir, cursor, origin):
    files_walker = AllFilesWalker()
    for extension, filename in files_walker.walk(contest_xmls_dir):
        contest_id = os.path.basename(filename)[:6]
        if not contest_id.isdigit():
            logging.warning('Invalid contest id {}'.format(contest_id))
            continue
        contest_name = ejudge_get_contest_name(filename)
        logging.info('Filling contest name for contest #{}'.format(contest_id))
        cursor.execute('UPDATE Contests SET name = ? WHERE origin = ? AND contest_id = ?',
                       (contest_name, origin, contest_id.rjust(6, '0')))
        if cursor.rowcount != 1:
            logging.warning('Contest #{} not found'.format(contest_id))
