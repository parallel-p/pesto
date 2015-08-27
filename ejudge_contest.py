import os
import logging


class EjudgeContest:
    def __init__(self, dir_name):
        self.problems = []
        self.polygon = {}
        self.dir_name = dir_name.rstrip('\\').rstrip('/')
        serve_filename = os.path.join(self.dir_name, 'conf', 'serve.cfg')
        try:
            file = open(serve_filename, encoding='utf-8')
            cfg_string = file.read().strip()
            file.close()
        except Exception:
            logging.error('Unable to read {}'.format(serve_filename))
        else:
            self.parse_config(cfg_string)

    def get_contest_id(self):
        return self.contest_id

    def get_problem_ids(self):
        return [(self.contest_id, pid) for pid in sorted(self.problems)]

    def get_short_name_by_problem_id(self, problem_id):
        return self.problems[problem_id[1]][0]

    def get_polygon_id_by_problem_id(self, problem_id):
        return self.polygon.get(problem_id[1], '')

    def get_test_paths_by_problem_id(self, problem_id):
        res = []
        test_num = 0
        if self.problems[problem_id[1]][1] is None or not self.test_pattern or not self.corr_pattern:
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
        cfg = [line for line in cfg if not line.startswith('#')]
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
            logging.warning('test_pat not found in contest {}'.format(self.contest_id))
            self.test_pattern = None
        if 'corr_pat' in sect:
            self.corr_pattern = sect['corr_pat'].strip('"')
        elif 'corr_sfx' in sect:
            self.corr_pattern = '%03d' + sect['corr_sfx'].strip('"')
        else:
            logging.warning('corr_pat not found in contest {}'.format(self.contest_id))
            self.corr_pattern = None

    def get_problems(self, cfg):
        cfg = '\n'.join(cfg).split('[problem]')[1:]
        if '[tester]' in cfg[-1]:
            cfg[-1] = cfg[-1].split('[tester]')[0]
        cfg = [self.parse_section(sect) for sect in cfg]
        self.get_patterns(cfg[0])

        problems = {}
        paths = {}
        if self.test_pattern:
            try:
                self.test_pattern % 1
            except ValueError:
                logging.error('Invalid test pattern "{}" in {}'.format(self.test_pattern,
                                                                       os.path.join(self.dir_name, 'conf',
                                                                                    'serve.cfg')))
            else:
                for root, dirs, files in os.walk(self.dir_name):
                    try:
                        if (self.test_pattern % 1) in files:
                            shortname = root.rstrip('tests').rstrip(os.path.sep).split(os.path.sep)[-1]
                            paths[shortname] = root
                            logging.debug(
                                'Cases for problem {} from contest {} found in {}'.format(shortname, self.contest_id,
                                                                                          root))
                    except Exception:
                        logging.exception('Exception caught')  # is it possible to get an exception here?
        for problem in cfg:
            try:
                if 'abstract' in problem:
                    continue
                if 'internal_name' in problem:
                    problem['short_name'] = problem['internal_name']
                problem['short_name'] = problem['short_name'].strip('"')
                problems[problem['id']] = (problem['short_name'], paths.get(problem['short_name']))
                if 'extid' in problem:
                    problem['extid'] = problem['extid'].strip('"')
                    if problem['extid'].startswith('polygon:'):
                        self.polygon[problem['id']] = problem['extid'].lstrip('polygon:')
            except KeyError as e:
                logging.error('Invalid problem in contest {}, {} missing'.format(self.contest_id, str(e)))
        return problems


    def parse_section(self, sect):
        sect = sect.strip().splitlines()
        sect = [line.split(' = ', maxsplit=1) if ' = ' in line else (line, None) for line in sect]
        return dict(sect)
