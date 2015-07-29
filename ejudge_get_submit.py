import xml.etree.ElementTree as ETree
from run_class import Run
from problem import Problem
from submit import Submit


def ejudge_get_submit(file, memory_base, contest_id):
    lines = file.readlines()
    if type(lines[0]) == type(b''):
        for i in range(len(lines)):
            lines[i] = lines[i].decode()
    data = ''.join(lines[2:])
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        return None
    runs = []
    problem, submit_id, user_id, submit_outcome = None, None, None, None
    for child in xml_root.iter():
        if child.tag == 'testing':
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
    if None in (problem, submit_id, user_id, submit_outcome):
        return None
    return Submit(submit_id, problem, user_id, runs, submit_outcome)