# Функция вызывается от того же filename, что и функция, создающая csv-файл,
# поэтому нет смысла проверять файл на существование


def max_test_cases(filename):
    file = open(filename)
    result = dict()
    for line in file:
        contest_id, problem_id, test_numbers = line.strip('\n').split(';')
        result[(contest_id, problem_id)] = int(test_numbers)
