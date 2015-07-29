import xml.etree.ElementTree as ETree
from run import Run
from problem import Problem
from submit import Submit


def ejudge_get_submit(file, memory_base, contest_id):
    lines = file.readlines()
    if type(lines[0]) == bytes:
        for i in range(len(lines)):
            lines[i] = lines[i].decode()
    # Removing first two lines, because they are not XML
    data = ''.join(lines[2:])
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        return None
    runs = []
    submit_id, problem, user_id, submit_outcome = None, None, None, None
    for child in xml_root.iter():
        if child.tag == 'testing-report':
            submit_id = child.attrib['run-id']
            submit_outcome = child.attrib['status']
            problem_id = memory_base.database.get_problem_id(contest_id, submit_id)
            user_id = memory_base.database.get_user_id(contest_id, submit_id)
            if memory_base.problem_exists(contest_id, problem_id):
                problem = memory_base.get_problem(contest_id, problem_id)
            else:
                case_ids = [x + 1 for x in range(int(child.attrib['run-tests']))]
                problem = Problem(contest_id, problem_id, case_ids)
                memory_base.add_problem(contest_id, problem_id, problem)
        elif child.tag == 'test':
            runs.append(Run(problem, submit_id, child.attrib['num'], child.attrib['status']))
    # If we haven't visit the 'testing-report' tag, we can't say anything about submit
    if None in (submit_id, problem, user_id, submit_outcome):
        return None
    return Submit(submit_id, problem, user_id, runs, submit_outcome)