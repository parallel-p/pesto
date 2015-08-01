from visitor import Visitor


class SameRuns(Visitor):

    def __init__(self):
        super().__init__()
        self.connected_components = []
    
    def visit(self, matrix):
        for i in range(len(matrix.result)):
            for j in range(len(matrix.result)):
                if i == j:
                    continue
                if matrix.result[i][j] == len(matrix.runs_id) / len(matrix.result):
                    f = False
                    for component in self.connected_components:
                        if i in component:
                            component.add(matrix.runs_id[j])
                            f = True
                        if j in component:
                            component.add(matrix.runs_id[i])
                            f = True
                    if not f:
                        self.connected_components.append(set([matrix.runs_id[i], matrix.runs_id[j]]))
        
    #self.result = connected_components
    
    def pretty_print(self):
        print_data = ""
        for component in self.connected_components:
            print_data += " ".join(map(str, component)) + "\n"
        return print_data

    def get_stat_data(self):
        return self.connected_components


classname = "SameRuns"