import os


class EjudgeContest:
    def __init__(self, dir_name):
        self.problems = []
        self.dir_name = dir_name.rstrip('\\').rstrip('/')

        file = open(os.path.join(self.dir_name, 'conf', 'serve.cfg'), encoding='utf-8')
        cfg_string = file.read().strip()
        file.close()
        self.parse_config(cfg_string)

    def get_contest_id(self):
        return self.contest_id

    def get_problem_ids(self):
        return [(self.contest_id, pid) for pid in sorted(self.problems)]

    def get_short_name_by_problem_id(self, problem_id):
        return self.problems[problem_id[1]][0]

    def get_test_paths_by_problem_id(self, problem_id):
        res = []
        test_num = 0
        if self.problems[problem_id[1]][1] is None:
            return []
        while 1:
            test_num += 1
            test_name = self.problems[problem_id[1]][1] + os.path.sep + self.test_pattern % test_num
            corr_name = self.problems[problem_id[1]][1] + os.path.sep + self.corr_pattern % test_num
            if not os.path.isfile(test_name) or not os.path.isfile(corr_name):
                break
            res.append((test_name, corr_name))
        return res

    def parse_config(self, cfg_string):
        cfg = cfg_string.splitlines(keepends=False)
        self.contest_id = self.get_param(cfg, 'contest_id') or os.path.basename(self.dir_name).lstrip('0')
        self.scoring = self.get_param(cfg, 'score_system')
        self.languages = self.get_languages(cfg)
        self.problems = self.get_problems(cfg)

    def get_param(self, cfg, name):
        for i in cfg:
            if i.startswith(name):
                return i.split(' = ')[1]
        return ''

    def get_languages(self, cfg):
        langs = {}
        cur_id = None
        is_lang_section = 0
        for i in cfg:
            if not i:
                continue
            if i[0] == '[':
                is_lang_section = (i == '[language]')
            elif not is_lang_section:
                continue
            elif i.startswith('id '):
                cur_id = i.split(' = ')[1]
            elif i.startswith('short_name '):
                langs[cur_id] = i.split(' = ')[1]
                cur_id = None
        return langs

    def get_patterns(self, sect):
        if 'test_pat' in sect:
            self.test_pattern = sect['test_pat'].strip('"')
        elif 'test_sfx' in sect:
            self.test_pattern = '%03d' + sect['test_sfx'].strip('"')
        else:
            self.test_pattern = '%03d'
        if 'corr_pat' in sect:
            self.corr_pattern = sect['corr_pat'].strip('"')
        elif 'corr_sfx' in sect:
            self.corr_pattern = '%03d' + sect['corr_sfx'].strip('"')
        else:
            self.corr_pattern = '%03d'

    def get_problems(self, cfg):
        cfg = '\n'.join(cfg).split('[problem]')[1:]
        if '[testing]' in cfg[-1]:
            cfg[-1] = cfg[-1].split('[testing]')[0]
        cfg = [self.parse_section(sect) for sect in cfg]
        self.get_patterns(cfg[0])

        problems = {}
        paths = {}
        for root, dirs, files in os.walk(self.dir_name):
            if (self.test_pattern % 1) in files:
                if root.endswith('tests'):
                    shortname = root.rstrip('tests').rstrip(os.path.sep).split(os.path.sep)[-1]
                else:
                    shortname = root.split(os.path.sep)[-1]
                paths[shortname] = root

        for problem in cfg[1:]:
            if 'internal_name' in problem:
                problem['short_name'] = problem['internal_name']
            problem['short_name'] = problem['short_name'].strip('"')
            problems[problem['id']] = (problem['short_name'], paths.get(problem['short_name']))
        return problems


    def parse_section(self, sect):
        sect = sect.strip().splitlines()
        sect = [line.split(' = ') for line in sect if ' = ' in line]
        return dict(sect)
