from visitor import Visitor


class EqMatrix(Visitor):
    def __init__(self):
        super().__init__()
        self.result = []
        self.runs_num = 0

    def visit(self, submit):
        case_amount = len(submit.runs)  # amount of cases in this submit

        self.runs_num += len(submit.runs)  # for same_runs.py

        if case_amount > len(self.result):  # extending matrix in case we found more cases
            for i in range(len(self.result)):
                self.result[i].extend([0] * (case_amount - len(self.result)))
            self.result.extend([[0] * case_amount for i in range(case_amount - len(self.result))])

        for i in range(case_amount):
            for j in range(case_amount):
                comp_list = []  # this is needed in order to unite "WA", "ML" etc
                if submit.runs[i].outcome == "OK":
                    comp_list.append(1)
                else:
                    comp_list.append(0)
                if submit.runs[j].outcome == "OK":
                    comp_list.append(1)
                else:
                    comp_list.append(0)
                if comp_list[0] == comp_list[1]:
                    self.result[i][j] += 1

    def pretty_print(self):
        print_data = ""
        for line in self.result:
            results = " ".join(map(str, line)) + "\n"
            print_data += results
        return print_data

