from memory_database import MemoryDatabase
import os.path

# Returns a dictionary of dictionaries of submit count by number of cases by problem id
def submits_over_numbers_histogram(home_dir, database_filename):
    database = MemoryDatabase(home_dir, database_filename)
    result = dict()
    for problem in database.problems.values():
        submits_count_by_cases_number = dict()
        cases_by_submits = dict()
        for submit in problem.get_submits(database):
            cases_by_submits[submit] = [run.case_id for run in submit.runs]
        for submit in cases_by_submits.keys():
            cases_number = len(cases_by_submits[submit])
            if cases_number not in submits_count_by_cases_number:
                submits_count_by_cases_number[cases_number] = 1
            else:
                submits_count_by_cases_number[cases_number] += 1
        result[problem.problem_id] = submits_count_by_cases_number
    return result


if __name__ == '__main__':

    data = submits_over_numbers_histogram(os.path.join('..', '000017'),
                                          os.path.join('..', 'runs.csv'))
    fout = open('histogram.txt', 'w')
    print(data[data.keys()[0]], file=fout)
    fout.close()
