from os.path import join
import os


class EjudgeContest():
    def __init__(self, dir_name):
        self.problems_list = []
        self.tests_paths_list = []

        self.dir_name = dir_name
        self._cfg_file = None

    def parse_contest(self):
        self.cfg_file = open(join(self.dir_name, 'conf', 'serve.cfg'))
        self.parse_cfg()

        if 'problems' in os.lsdir():
            self.is_standart = True
        else:
            self.is_standart = False

    def _parse_cfg(self, dir_name):
        config_file_contet = self.cfg_file.read()
        self.problems_list = self._find_problems(config_file_contet)
        self.contest_id = self._find_contest_id(config_file_contet)


    def _find_problems(self, cfg_cont):
        config_file_contet = cfg_cont.split('[problem]')
        if ('[tester]' in config_file_contet[-1]):
            self.cfg_file[-1] = config_file_contet[-1].split('[tester]')[0]
        problems_list = []
        for problem in config_file_contet:
            problems_list.append(dict())
            for exp in problem.split('\n'):
                if '=' in exp:
                    key, val = exp.split(' = ')
                    problems_list[-1][key] = val
        return problems_list

    def _find_contest_id(self, cfg_cont):
        config_file_contet = cfg_cont.split('\n')
        for line in config_file_contet:
            if 'contest_id' in line:
                return line.split(' = ')[1]

    def get_tests_paths_by_problem_id(self, id):
        pass

    def get_short_name_by_problem_id(self, id):
        for problem in self.problems_list:
            if ('id' in problem) and (problem['id'] == id):
                return problem['short_name']

    def get_contest_id(self):
        return self.contest_id

    def get_problems_ids(self):
        return [self.problem['id'] for problem in self.problems_list]