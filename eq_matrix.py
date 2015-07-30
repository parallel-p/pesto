from submit import Submit

def get_eq_matrix(submits):
    case_amount = len(submits[0].problem.case_ids) # as submits refer to same problem, case am. should be same

    for i in range(case_amount):
        matrix.append([0] * case_amount)

    for first in range(case_amount):
        for second in range(first + 1, case_amount): # warning! Half of the table is left filled with 0!
            for submit in submits:
                comp_list = [] # this is needed in order to unite "WA", "ML" etc as fail
                if submit[first] == "OK":
                    comp_list.append(1)
                else:
                    comp_list.append(0)
                if submit[second] == "OK":
                    comp_list.append(1)
                else:
                    comp_list.append(0)
                    
                if comp_list[0] == comp_list[1]:
                    matrix[first][second] += 1
    return matrix
