from visitor import Visitor


def sec_to_time(sec):
    s = str(sec % 60) + 'S'
    sec //= 60
    m = str(sec % 60) + 'M '
    sec //= 60
    h = str(sec % 24) + 'H '
    sec //= 24
    d = str(sec % 365) + 'D '
    return d + h + m + s


class SameRunsBigStat(Visitor):
    def __init__(self):
        super().__init__()
        self.cases = 0
        self.cases_to_del = 0
        self.time = 0
        self.time_to_del = 0

        self.base = {}

    def visit(self, submit):
        name = submit.problem_id
        if name not in self.base.keys():
            if submit.scoring == 'ACM':
                self.base[name] = SameRunsACM()
            else:
                self.base[name] = SameRunsKirov()
        self.base[name].visit(submit)

    def pretty_print(self):
        for same_runs in self.base.values():
            try:
                same_runs.calc()
                same_runs.xcalc()
                self.cases += same_runs.cases
                self.cases_to_del += same_runs.cases_to_del
                self.time += same_runs.time
                self.time_to_del += same_runs.time_to_del
            except:
                pass

        result = ''
        if self.cases != 0:
            result += 'WE RECOMMEND REMOVING: {0}/{1} ({2}%)'.format(self.cases_to_del, self.cases,
                                                                     int(100 * self.cases_to_del / self.cases)) + '\n'
        else:
            result += 'DEV BY ZERO\n'
        if self.time != 0:
            result += 'IT WILL SAVE: {0} / {1} ({2}%)'.format(sec_to_time(int(self.time_to_del / 1000)),
                                                              sec_to_time(int(self.time / 1000)),
                                                              int(100 * self.time_to_del / self.time)) + '\n'
        else:
            result += 'DEV BY ZERO\n'
        return result


class SameRuns(Visitor):
    def __init__(self):
        super().__init__()
        self.submit_number = 0
        self.connected_components = []
        self.strong_runs = set()
        self.times = {}

        self.bad_cases = set()

        self.cases = 0
        self.cases_to_del = 0
        self.time = 0
        self.time_to_del = 0

        self.problem_id = ()

    def get_stat_data(self):
        """int, list of sets of ints, set of ints"""
        return [self.run_number, self.connected_components, self.strong_runs]

    def pre_visit(self, submit):
        self.problem_id = submit.problem_id
        self.cases = max(self.cases, len(submit.runs))
        self.submit_number += 1
        for run in submit.runs:
            self.time += int(run.time)
            if run.case_id not in self.times.keys():
                self.times[run.case_id] = [1, int(run.time)]
            else:
                self.times[run.case_id][0] += 1
                self.times[run.case_id][1] += int(run.time)

    def calc(self):
        pass

    def xcalc(self):
        self.cases_to_del = self.cases - len(self.strong_runs) - len(self.connected_components)
        self.bad_cases = set()
        self.time_to_del = 0
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
                    self.bad_cases.add(case)
            self.time_to_del += sm - self.times[boss][1]

        self.time = 0
        for time in self.times.values():
            self.time += time[1]

    def pretty(self):
        result = 'Submits - {0}\n'.format(self.submit_number)
        if len(self.connected_components) > 0:
            components = [list(comp) for comp in self.connected_components]
            components = [list(map(int, comp)) for comp in components]
            components = [sorted(comp) for comp in components]
            components.sort()
            components = [list(map(str, comp)) for comp in components]
            components = ['{' + ' '.join(comp) + '}' for comp in components]
            result += 'Equivalent tests: ' + ' '.join(components) + '\n'  # so cute
        if len(self.strong_runs) > 0:
            result += 'Unique tests: {' + ' '.join(map(str, sorted(self.strong_runs, key=int))) + '}\n'

        self.xcalc()

        if self.bad_cases:
            if self.cases != 0:
                result += 'we recommend removing: {0}/{1} ({2}%) '.format(self.cases_to_del, self.cases, int(
                    100 * self.cases_to_del / self.cases)) + '{' + ' '.join(
                    map(str, sorted(self.bad_cases, key=int))) + '}\n'
            else:
                result += 'DEV BY ZERO\n'
            if self.time != 0:
                result += 'it will save: {0}sec/{1}sec ({2}%)'.format(int(self.time_to_del / 1000),
                                                                      int(self.time / 1000),
                                                                      int(100 * self.time_to_del / self.time)) + '\n'
            else:
                result += 'DEV BY ZERO\n'
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
        if len(submit.runs) == 0:
            return
        if submit.runs[-1].outcome != 'OK':
            self.base.add(len(submit.runs) - 1)
        else:
            self.base.add(len(submit.runs))

        if (len(submit.runs) > self.mx):
            self.mx = len(submit.runs)
            self.runs = [x.case_id for x in submit.runs]

    def calc(self):
        self.connected_components = []
        self.strong_runs = set()
        self.runs.append(int(self.runs[-1]) + 1)
        left = 0
        for right in sorted(self.base):
            if right == 0:
                continue
            if right - left == 1:
                self.strong_runs.add(self.runs[left])
            else:
                self.connected_components.append(set(self.runs[i] for i in range(left, right) if i < len(self.runs)))
            left = right

    def pretty_print(self):
        try:
            self.calc()
            return self.pretty()
        except:
            pass


"""
   _        _
  ( `-.__.-' )
   `-.    .-'
      \  /
       ||
       ||
      //\\
     //  \\
    ||    ||
    ||____||
    ||====||
     \\  //
      \\//
       ||
       ||
       ||
       ||
       ||
       ||
       ||
       ||
       []

git kill --hard vanya
"""
