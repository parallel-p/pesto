# This function and the function creating the csv file is called from the same filename
# so there is no need to check the file for existence


def max_test_cases(filename):
    file = open(filename)
    result = dict()
    for line in file:
        contest_id, problem_id, test_numbers = line.strip('\n').split(';')
        result[(contest_id, problem_id)] = int(test_numbers)
    file.close()
    return result