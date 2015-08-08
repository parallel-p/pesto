from visitor import Visitor


class SameRuns(Visitor):
    def __init__(self):
        super().__init__()
        self.submit_number = 0
        self.connected_components = []
        self.strong_runs = set()
        self.times = {}

    def get_stat_data(self):
        return [self.run_number, self.connected_components, self.strong_runs]  # int, list of sets of ints, set of ints

    def pre_visit(self, submit):
        self.submit_number += 1
        for run in submit.runs:
            if run.case_id not in self.times.keys():
                self.times[run.case_id] = [1, int(run.time)]
            else:
                self.times[run.case_id][0] += 1
                self.times[run.case_id][1] += int(run.time)

    def pretty(self):
        result = 'Submits - {0}\n'.format(self.submit_number)
        if len(self.connected_components) > 0:
            result += 'Equivalent tests: ' + ' '.join(map(lambda component: '{' + (' '.join(map(str, sorted(component))) + '}'),
                                                          sorted(self.connected_components))) + '\n'
        if len(self.strong_runs) > 0:
            result += 'Unique tests: {' + ' '.join(map(str, sorted(self.strong_runs))) + '}\n'

        bad_cases = set()
        big_sum = 0
        for component in self.connected_components:
            mn = float('Inf')
            sm = 0
            for run in component:
                sm += self.times[run][1]
                if mn > self.times[run][1] / self.times[run][0]:
                    mn = self.times[run][1] / self.times[run][0]
                    boss = run
            for case in component:
                if case != boss:
                    bad_cases.add(case)
            big_sum += sm - self.times[boss][1]

        if bad_cases:
            result += 'we recommend removing: {' + ' '.join(map(str, sorted(bad_cases))) + '}\n'
            result += 'it will save: {0}sec'.format(big_sum / 1000)

        return result


class SameRunsKirov(SameRuns):
    def __init__(self):
        super().__init__()

    def visit(self, submit):
        if (self.submit_number == 0):
            self.connected_components.append(run.case_id for run in submit.runs)

        self.pre_visit(submit)
        temp_connected_components = []

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
        return self.pretty()


class SameRunsACM(SameRuns):
    def __init__(self):
        super().__init__()
        self.base = set()
        self.mx = 0
        self.runs = []

    def visit(self, submit):
        self.pre_visit(submit)
        if submit.runs[-1].outcome != 'OK':
            self.base.add(len(submit.runs) - 1)
        else:
            self.base.add(len(submit.runs))

        if (len(submit.runs) > self.mx):
            self.mx = len(submit.runs)
            self.runs = [x.case_id for x in submit.runs]

    def calc(self):
        self.runs.append(self.runs[-1] + 1)
        left = 0
        for right in sorted(self.base):
            if right == 0:
                continue
            if right - left == 1:
                self.strong_runs.add(self.runs[left])
            else:
                self.connected_components.append(set(self.runs[i] for i in range(left, right)))
            left = right

    def pretty_print(self):
        self.calc()
        return self.pretty()
