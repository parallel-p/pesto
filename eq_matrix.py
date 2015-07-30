def get_eq_matrix(submits):
    case_amount = len(submits[0].problem.case_ids) # as submits refer to same problem, which knows max cases amount
    
    matrix = [[0] * case_amount for i in range(case_amount)]

    for submit in submits:
        for first in range(len(submit.runs)):
            for second in range(len(submit.runs)): 
                comp_list = [] # this is needed in order to unite "WA", "ML" etc
                if submit.runs[first].outcome == "OK":
                    comp_list.append(1)
                else:
                    comp_list.append(0)
                if submit.runs[second].outcome == "OK":
                    comp_list.append(1)
                else:
                    comp_list.append(0)
                if comp_list[0] == comp_list[1]:
                    matrix[first][second] += 1
    return matrix
