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

    def get_stat_data(self):
        result = []
        for key_visitor in sorted(self.visitors.items()):
            result.append((key_visitor[0], key_visitor[1].get_stat_data()))
        return result

    def pretty_key(self, key):
        return str(key)

    def pretty_print(self):
        result = ''
        for key in sorted(self.visitors.keys()):
            child_result = self.visitors[key].pretty_print()
            if child_result in ['', None]:
                continue
            result += '\n' + self.pretty_key(key) + ':\n\t' + child_result.replace('\n', '\n\t')
        return result

    def build_key(self, submit):
        return str(submit)


class ShardingByProblemVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id

    def pretty_key(self, key):
        return 'Contest #{}, Problem #{}'.format(key[0], key[1])


class ShardingByContestVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.problem_id[0]

    def pretty_key(self, key):
        return 'Contest #{}'.format(key)


class ShardingByUserVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.user_id

    def pretty_key(self, key):
        return 'UserID #{}'.format(key)


class ShardingByLangVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.lang_id

    def pretty_key(self, key):
        return 'LangID #{}'.format(key)


class ShardingByScoringVisitor(ShardingVisitor):
    def build_key(self, submit):
        return submit.scoring

    def pretty_key(self, key):
        return 'Scoring type - #{}'.format(key)