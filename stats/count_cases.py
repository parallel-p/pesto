from memory_database import MemoryDatabase


def count_cases(problems, contest_id): # dict of problems goes here with key
    _result = []
    for problem_pair in problems.items():    # problem_pair[0] - key of dict item
        if problem_pair[0][0] == contest_id: # problem_pair[0][0] - contest_id in key
            problem = problem_pair[1]        # problem_pair[1] - value of dict item
            _result.append((problem.contest_id, problem.problem_id, len(problem.case_ids)))
    _result.sort()
    return _result

def main():
    print('Enter contests base dir name:')
    base_dir = input()
    print('Enter database filename:')
    database_filename = input()
    print('Enter contest ID')
    contest_id = input()
    database = MemoryDatabase(base_dir, database_filename)
    return (database.problems, contest_id)


if __name__ == "__main__":
    problems, contest_id = main()
    for result in count_cases(problems, contest_id):
        print("Contest ID #{0}, Problem ID #{1}\tCases amount: {2}".format(*result))
