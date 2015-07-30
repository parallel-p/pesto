import os.path
from run import Run
from submit import Submit
from problem import Problem
from ejudgedb import EjudgeDB
from traverse import traverse_contest
from ejudge_xml_parse import ejudge_xml_parse


def ejudge_parse(contest_dirs, csv_filename):
    database = EjudgeDB(csv_filename)
    problems, submits = dict(), []
    for contest_dir in contest_dirs:
        contest_id = os.path.basename(contest_dir)
        if contest_id.isdigit():
            contest_id = contest_id.lstrip('0')
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
            if problem_id is None or user_id is None:
                continue
            case_ids = [str(x + 1) for x in range(len(run_outcomes))]
            if (contest_id, problem_id) in problems:
                problem = problems[(contest_id, problem_id)]
                problem.case_ids = list(set(problem.case_ids + case_ids))
            else:
                problem = Problem(contest_id, problem_id, case_ids)
                problems[(contest_id, problem_id)] = problem
            runs = [Run(problem, submit_id, i + 1, run_outcomes[i]) for i in range(len(run_outcomes))]
            submits.append(Submit(submit_id, problem, user_id, runs, submit_outcome))
    return problems, submits
