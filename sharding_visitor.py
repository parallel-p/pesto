from visitor import Visitor


class ShardingVisitor(Visitor):
    def __init__(self, factory):
        super().__init__()
        self.visitors = dict()
        self.factory = factory

    def visit(self, submit):
        key = self.build_key(submit)
        if key not in self.visitors:
            self.visitors[key] = self.factory.create(key)
        self.visitors[key].visit(submit)

    def _enum_visitors(self):
        result = list(self.visitors.items())
        try:
            result.sort(key=lambda p: self._comparable_key(p[0]))
        except Exception:
            result.sort()
        return result

    def comparable_key(self, key):
        return int(key)

    def _comparable_key(self, key):
        try:
            return self.comparable_key(key)
        except Exception:
            return key

    def get_stat_data(self):
        result = []
        for key, visitor in self._enum_visitors():
            result.append((key, visitor.get_stat_data()))
        return result

    def pretty_key(self, key):
        return str(key)

    def pretty_print(self):
        result = ''
        for key, visitor in self._enum_visitors():
            child_result = visitor.pretty_print()
            if child_result in ['', None]:
                continue
            result += '\n' + self.pretty_key(key) + ':\n\t' + child_result.replace('\n', '\n\t')
        return result

    def build_key(self, submit):
        return str(submit)


class ShardingByProblemVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id

    def comparable_key(self, key):
        return int(key[1])

    def pretty_key(self, key):
        return 'Problem #{}'.format(key[1])


class ShardingByContestVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id[0]

    def pretty_key(self, key):
        return 'Contest #{}'.format(key)


class ShardingByUserVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.user_id

    def pretty_key(self, key):
        return 'User #{}'.format(key)


class ShardingByLangVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.lang_id

    def pretty_key(self, key):
        return 'Lang #{}'.format(key)


class ShardingByScoringVisitor(ShardingVisitor):
    def build_key(self, submit):
        return 'ACM' if submit.scoring == 'ACM' else 'kirov'

    def pretty_key(self, key):
        return 'Scoring type: {}'.format(key)
