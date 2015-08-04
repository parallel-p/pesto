from visitor import Visitor


class SameRunsKirov(Visitor):

    def __init__(self):
        super().__init__()
        self.run_number = 0
        self.submit_number = 0
        self.connected_components = []
        self.strong_runs = set()

    def get_stat_data(self):
        return self.connected_components

    def visit(self, submit):
        self.submit_number += 1
        temp_connected_components = []

        if (len(submit.runs) > self.run_number):
            self.connected_components.append(submit.runs[i].case_id for i in range(self.run_number, len(submit.runs)))
            self.run_number = len(submit.runs)

        for component in self.connected_components:
            first, second = set(), set()
            for i in range(len(submit.runs)):
                if submit.runs[i].case_id in component:
                    if submit.runs[i].outcome == 'OK':
                        first.add(submit.runs[i].case_id)
                    else:
                        second.add(submit.runs[i].case_id)

            if len(first) == 1:
                self.strong_runs.add(list(first)[0])
            if len(second) == 1:
                self.strong_runs.add(list(second)[0])
            if len(first) > 1:
                temp_connected_components.append(first)
            if len(second) > 1:
                temp_connected_components.append(second)
        self.connected_components = temp_connected_components

    def pretty_print(self):

        result = 'Submits - {0}\n'.format(self.submit_number)
        if len(self.connected_components) > 0:
            result += 'Equivalent tests: ' + ' '.join(map(lambda component: '{' + (' '.join(map(str, component)) + '}'),
                                                          self.connected_components)) + '\n'
        if len(self.strong_runs) > 0:
            result += 'Unique tests: {' + ' '.join(map(str, self.strong_runs)) + '}\n'
        return result


classname = "SameRunsKirov"
