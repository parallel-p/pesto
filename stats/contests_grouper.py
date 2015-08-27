import re


SEASON_TO_INT = {'': -1, 'Июль': 0, 'Август': 1, 'Николаев': 2, 'Подмосковье': 3, 'Зима': 4}
PARALLEL_TO_INT = {
    '': -1,
    'A': 0,
    'A\'': 1,
    'A0': 2,
    'AA': 3,
    'AS': 4,
    'AY': 5,
    'B': 6,
    'B\'': 7,
    'C': 8,
    'C\'': 9,
    'Ccpp': 8,
    'Cpy': 10,
    'D': 11,
    'olymp': 12,
    'A+': 0,
    'A\'+': 1,
    'A0+': 2,
    'AA+': 3,
    'AS+': 4,
    'AY+': 5,
    'B+': 6,
    'B\'+': 7,
    'C+': 8,
    'C\'+': 9,
    'Ccpp+': 8,
    'Cpy+': 10,
    'D+': 11,
}


class _Contest:
    def __init__(self, year, season, day, parallel):
        self.year = year
        self.season = season
        self.day = day
        self.parallel = parallel

    def get_key(self):
        return self.year, SEASON_TO_INT[self.season], self.day, PARALLEL_TO_INT[self.parallel.rstrip('+')]


class ContestsGrouper:
    def __init__(self, contests):
        self.contests = dict()
        self.contests_sorted = []

        year_regex = re.compile('20[0-9]{2}')
        parallel_regex = re.compile('(?:' + re.escape('.') + '|\\s)' +
                                    '(?:[ABCDZСА]|AS|AA|AY)(?:\.?py|\.?python|prime|' +
                                    '\.?' + re.escape('c++') + '|' + re.escape('++') + '|\.?cpp|[0-9]+|' +
                                    re.escape('\'') + ')?' + re.escape('+') +
                                    '?(?:' + re.escape('.') + '|\\s|$)')
        season_regex = re.compile('(?:Июль|Август|Зима|Николаев|Подмосковье)', re.I)
        day_regex = re.compile(
            '(?:(?:день|day)(?:\\s|\\.)*[0-9]{1,2}|(?:(?:\\s|\\.|D)[0-9]{1,2}(?:\\s|\\.|[^0-9]|$))(?!(?:день|day)))',
            re.I)

        parallels = set()

        for contest in contests:

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
                parallel = re.sub('\\s', '', parallel_regex.findall(contest.name)[0].replace('.', ''))
                parallel = re.sub('prime', '\'', parallel)
                parallel = re.sub('python', 'py', parallel)
                parallel = re.sub(re.escape('c++'), 'cpp', parallel)
                parallel = re.sub(re.escape('++'), 'cpp', parallel)
                parallel = re.sub(re.escape('С'), 'C', parallel)  # Russian letters!
                parallel = re.sub(re.escape('А'), 'A', parallel)
                if parallel.startswith('D') and parallel != 'D':
                    parallel = 'D'
            if not season_regex.findall(contest.name):
                season = ''
            else:
                season = season_regex.findall(contest.name)[0]
            if 'зачет' in contest.name.lower() or 'зачёт' in contest.name.lower() or 'зачот' in contest.name.lower() or 'exam' in contest.name.lower():
                day = 'exam'
            elif not day_regex.findall(contest.name):
                day = ''
            else:  # This replaces is also dangerous.
                day = day_regex.findall(contest.name)[0]
                day = re.sub('\\s', '', day)
                day = re.sub('\\.', '', day)
                day = re.sub('(?:день|day)', '', day, flags=re.I)
                day = day.lstrip('D')
                day = day.lstrip('d')
                day = day.lstrip('0')
                day = re.sub('[^0-9]', '', day)

            self.contests[contest.contest_id] = _Contest(year, season, day, parallel)
            self.contests_sorted.append(contest)
            parallels.update({parallel})

        self.contests_sorted.sort(key=lambda x: self.contests[x.contest_id].get_key())

    def get_contest_year_by_id(self, contest_id):
        return self.contests[contest_id].year

    def get_contest_season_by_id(self, contest_id):
        return self.contests[contest_id].season

    def get_contest_parallel_by_id(self, contest_id):
        return self.contests[contest_id].parallel

    def get_contest_day_by_id(self, contest_id):
        return self.contests[contest_id].day

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

    def group_contests_by_day(self, contest_ids):
        return self._group_contests_by_key(contest_ids, 'day')

    def get_all_known_contests(self):
        return self.contests.keys()

    def get_contests_sorted(self):
        return self.contests_sorted
