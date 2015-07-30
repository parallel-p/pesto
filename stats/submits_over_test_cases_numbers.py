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


def pretty_printer(data): # Takes data from submits_over_number_histogram()
    fout = open('histogram.txt', 'w')
    for problem in data.keys():

        cases_numbers = []
        submit_numbers = []
        for case_number in data[problem].keys():
            cases_numbers.append(case_number)
            submit_numbers.append(data[problem][case_number])
        bar_length_multiplier = int(80 / max(submit_numbers))
        print('------------\n'
              'Problem #{0}\n'
              '------------'.format(problem), file=fout)
        for i in range(len(cases_numbers)):

            print('{0:{width}}'.format(cases_numbers[i], width=5),
                  '#' * submit_numbers[i] * bar_length_multiplier,
                  submit_numbers[i], file=fout)
    fout.close()


if __name__ == '__main__':
    hist_data = submits_over_numbers_histogram(os.path.join('..', 'testdata',
                                                            'count_submit_test', '000017'),
                                               os.path.join('..', 'testdata',
                                                            'count_submit_test',
                                                            'mixed_runs_count_submit_test.csv'))
    pretty_printer(hist_data)
