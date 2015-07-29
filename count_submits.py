from memory_database import MemoryDatabase


def count_submits(base_dir, database_filename):
    database = MemoryDatabase(base_dir, database_filename)
    problems = dict()
    for problem in database.problems.values():
        problems[problem.problem_id] = 0
    for submit in database.submits:
        problems[submit.problem.problem_id] += 1
    return problems


if __name__ == '__main__':
    print('Enter contests base dir name:')
    base_dir = input()
    print('Enter database filename:')
    database_filename = input()
    print(count_submits(base_dir, database_filename))
