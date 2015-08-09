from ejudge_contest_xml import ejudge_get_contest_name
from walker import AllFilesWalker
import os


def fill_db_from_contest_xml(contest_xmls_dir, cursor, origin):
    files_walker = AllFilesWalker()
    for extension, filename in files_walker.walk(contest_xmls_dir):
        contest_name = ejudge_get_contest_name(filename)
        contest_id = os.path.basename(filename)[:6]
        cursor.execute('UPDATE Contests SET name = ? WHERE origin = ? AND contest_id = ?', (contest_name, origin, contest_id.ljust(6, '0')))