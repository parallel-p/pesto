from dao_contests import DAOContests
import re


class _Contest:
    def __init__(self, year, season, parallel):
        self.year = year
        self.season = season
        self.parallel = parallel


class ContestsGrouper:
    def __init__(self, contests_rows):
        self.contests = dict()

        year_regex = re.compile('20[0-9]{2}')
        parallel_regex = re.compile('(?:' + re.escape('.') + '|\\s)' +
                                    '(?:[ABCDPSKMZСА]|AS|AA|AY)(?:py|python|prime|' +
                                    re.escape('c++') + '|' + re.escape('++') + '|cpp|[0-9]+|' +
                                    re.escape('\'') + ')?' + re.escape('+') +
                                    '?(?:' + re.escape('.') + '|\\s|$)')
        season_regex = re.compile('(?:Июль|Август|Зима|Николаев|Подмосковье)', re.I)

        for row in contests_rows:
            contest = DAOContests.load(row)
            if contest.name is None:
                continue
            if 'ЛКШ' not in contest.name or 'template' in contest.name.lower():
                continue
            if not year_regex.findall(contest.name):
                year = 0
            else:
                year = int(year_regex.findall(contest.name)[0])
            if 'олимпиада' in contest.name.lower() or 'contest' in contest.name.lower() or 'соревнование' in contest.name.lower():
                parallel = 'olymp'
            elif not parallel_regex.findall(contest.name):
                parallel = ''
            else:  # Please, think twice, if you want to change this replaces.
                parallel = re.sub('\s', '', parallel_regex.findall(contest.name)[0].replace('.', ''))
                parallel = re.sub('prime', '\'', parallel)
                parallel = re.sub('python', 'py', parallel)
                parallel = re.sub(re.escape('c++'), 'cpp', parallel)
                parallel = re.sub(re.escape('++'), 'cpp', parallel)
                parallel = re.sub(re.escape('С'), 'C', parallel)  # Russian letters!
                parallel = re.sub(re.escape('А'), 'A', parallel)
            if not season_regex.findall(contest.name):
                season = ''
            else:
                season = season_regex.findall(contest.name)[0]

            self.contests[contest.contest_id] = _Contest(year, season, parallel)

    def get_contest_year_by_id(self, contest_id):
        return self.contests[contest_id].year

    def get_contest_season_by_id(self, contest_id):
        return self.contests[contest_id].season

    def get_contest_parallel_by_id(self, contest_id):
        return self.contests[contest_id].parallel

    def _group_contests_by_key(self, contest_ids, attr):
        result = dict()
        for contest_id in contest_ids:
            key = getattr(self.contests[contest_id], attr)
            if key not in result:
                result[key] = [contest_id]
            else:
                result[key].append(contest_id)
        return result

    def group_contests_by_year(self, contest_ids):
        return self._group_contests_by_key(contest_ids, 'year')

    def group_contests_by_season(self, contest_ids):
        return self._group_contests_by_key(contest_ids, 'season')

    def group_contests_by_parallel(self, contest_ids):
        return self._group_contests_by_key(contest_ids, 'parallel')

    def get_all_known_contests(self):
        return self.contests.keys()
