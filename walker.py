import os
from gzip import open as gzip_open
from ejudge_xml_parse import ejudge_xml_parse
from ejudgedb import EjudgeDB
from model import Run
from model import Submit
import pickle


class Walker:
    def walk(self, start_dir):
        yield None

class SingleContestWalker(Walker):
    def walk(self, start_dir):
        start_dir = start_dir.rstrip('/').rstrip('\\')
        yield (os.path.basename(start_dir).lstrip('0'), start_dir)

class MultipleContestWalker(Walker):
    def walk(self, start_dir = os.path.dirname(__file__)):
        for root, dirs, files in os.walk(start_dir):
            contest_id = os.path.split(root)[1]
            if ('conf' in dirs and ('problems' in dirs or 'tests' in dirs)
                               and contest_id.isdigit()
                               and len(contest_id) == 6):
                yield (contest_id.lstrip('0'), root)

class EjudgeRunsFilesWorker(Walker):
    def walk(self, start_dir):
        for dirname, _, filenames in os.walk(os.path.join(start_dir, 'var', 'archive', 'xmlreports')):
            for filename in filenames:
                file_full_name = os.path.join(dirname, filename)
                yield ('gzip' if filename.endswith('.gz') else 'xml', file_full_name)

class AllFilesWalker(Walker):
    def walk(self, start_dir):
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                if file.startswith('.'):
                    continue
                file_name = os.path.join(root, file)
                yield ('gzip' if file.endswith('.gz') else 'xml', file_name)

class PickleWorker(Walker):
    def walk(self, start_dir):
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                if not file.endswith('.pickle'):
                    continue

                file_name = os.path.join(root, file)
                yield ('pickle', file_name)

class SubmitWalker(Walker):
    def __init__(self, database_dir, contest_id):
        self.database = EjudgeDB(database_dir)
        self.contest_id = contest_id

    def walk(self, file_name):
        if file_name.endswith('.gz'):
            with gzip_open(file_name) as current_file:
             yield self._get_submit_from_xml(current_file)
        elif file_name.endswith('.pickle'):
            for submit in self._get_submit_from_pickle(file_name):
                yield submit
        else:
            with open(file_name, encoding='utf-8') as current_file:
                yield self._get_submit_from_xml(current_file)

    def _get_submit_from_pickle(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                arr = pickle.load(file)
        except pickle.UnpicklingError:
            pass
        for submit in arr:
            yield submit

    def _get_submit_from_xml(self, xml_file):
        try:
            result = ejudge_xml_parse(xml_file)
        except OSError:
            return None

        if result is None:
            return None
        submit_id = result.submit_id
        submit_outcome = result.submit_outcome
        run_outcomes = result.run_outcomes
        scoring = result.scoring
        problem_id = self.database.get_problem_id(self.contest_id, submit_id)
        user_id = self.database.get_user_id(self.contest_id, submit_id)
        lang_id = self.database.get_lang_id(self.contest_id, submit_id)

        if None in (problem_id, user_id):
            return None

        runs = [Run(problem_id, submit_id, i + 1, run_outcomes[i][0], run_outcomes[i][1], run_outcomes[i][2]) for i in range(len(run_outcomes))]
        submit = Submit(submit_id, (self.contest_id, problem_id), user_id, lang_id, runs, submit_outcome, scoring)
        return submit

