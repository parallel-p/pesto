import os.path
from model import Run
from model import Submit
from ejudgedb import EjudgeDB
from traverse import traverse_contest
from ejudge_xml_parse import ejudge_xml_parse


def ejudge_parse(contest_dirs, csv_filename, visitor):
    contest_ids = list()
    for i in range(len(contest_dirs)):
        contest_dirs[i] = contest_dirs[i].rstrip('/').rstrip('\\')
        contest_ids.append(os.path.basename(contest_dirs[i]))
        if contest_ids[i].isdigit():
            contest_ids[i] = contest_ids[i].lstrip('0')
    database = EjudgeDB(csv_filename, contest_ids)
    for contest_dir, contest_id in zip(contest_dirs, contest_ids):
        for file in traverse_contest(contest_dir):
            try:
                result = ejudge_xml_parse(file)
            except OSError:
                continue
            if result is None:
                continue
            submit_id = result.submit_id
            submit_outcome = result.submit_outcome
            run_outcomes = result.run_outcomes
            problem_id = database.get_problem_id(contest_id, submit_id)
            user_id = database.get_user_id(contest_id, submit_id)
            lang_id = database.get_lang_id(contest_id, submit_id)
            if None in (problem_id, user_id):
                continue
            runs = [Run(problem_id, submit_id, i + 1, run_outcomes[i]) for i in range(len(run_outcomes))]
            submit = Submit(submit_id, (contest_id, problem_id), user_id, lang_id, runs, submit_outcome)
            visitor.visit(submit)
