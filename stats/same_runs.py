from visitor import Visitor
from stats.eq_matrix import EqMatrix


class SameRuns(Visitor):

    def __init__(self):
        super().__init__()
        self.base_connected_components = {}
        self.base = {}
    
    def visit(self, submit):
        name = str(submit.problem_id[0]) + ' ' + str(submit.problem_id[1])
        if name not in self.base.keys():
            self.base[name] = EqMatrix()
            self.base_connected_components[name] = []
        matrix = self.base[name]
        connected_components = self.base_connected_components[name]

        matrix.visit(submit)

        for i in range(len(matrix.result)):
            for j in range(len(matrix.result)):
                if i == j:
                    continue
                if matrix.result[i][j] == matrix.runs_num / len(matrix.result):
                    f = False
                    for component in connected_components:
                        if i in component:
                            component.add(j)
                            f = True
                        if j in component:
                            component.add(i)
                            f = True
                    if not f:
                        connected_components.append(set([i, j]))
    
    def pretty_print(self):
        print_data = ""
        for name in self.base_connected_components.keys():
            print_data += str(name) + ':\n'

            for component in self.base_connected_components[name]:
                print_data += " ".join(map(str, component)) + "\n"
            return print_data

    def get_stat_data(self):
        return self.base_connected_components

classname = "SameRuns"