from memory_database import MemoryDatabase
import run


def get_all_submits():
    database = MemoryDatabase(base_dir, database_filename)
    problems = dict()
    problems_id = []

    for problem in database.problems.values():
        problems[problem.problem_id] = dict()
        problems_id += problem.problem_id
    for submit in database.submits:
        problem_id = problems[submit.problem.problem_id]
        runs_result = "".join(submit.runs)
        if (runs_result in problems[problem_id]):
            problems[problem_id][runs_result] += 1
        else:
            problems[problem_id][runs_result] = 0

    for problem_id in problems_id:
        print("Problem", problem_id)
        for runs_result in problems[problem_id]:
            for 




if __name__ == '__main__':
    print('Enter contests base dir name:')
    base_dir = input()
    print('Enter database filename:')
    database_filename = input()
    print(get_all_submits(base_dir, database_filename))