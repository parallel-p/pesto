from visitor import Visitor
from eq_matrix import EqMatrix


class SameRuns(Visitor):

    def __init__(self):
        super().__init__()
        self.connected_components = []
        self.matrix = EqMatrix()
    
    def visit(self, submit):
        self.matrix.visit(submit)

        for i in range(len(self.matrix.result)):
            for j in range(len(self.matrix.result)):
                if i == j:
                    continue
                if self.matrix.result[i][j] == len(self.matrix.runs_id) / len(self.matrix.result):
                    f = False
                    for component in self.connected_components:
                        if i in component:
                            component.add(self.matrix.runs_id[j])
                            f = True
                        if j in component:
                            component.add(self.matrix.runs_id[i])
                            f = True
                    if not f:
                        self.connected_components.append(set([self.matrix.runs_id[i], self.matrix.runs_id[j]]))
        
    #self.result = connected_components
    
    def pretty_print(self):
        print_data = ""
        for component in self.connected_components:
            print_data += " ".join(map(str, component)) + "\n"
        return print_data

    def get_stat_data(self):
        return self.connected_components


classname = "SameRuns"