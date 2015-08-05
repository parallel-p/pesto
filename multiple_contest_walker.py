import os
from walker import Walker


class MultipleContestWalker(Walker):
    def walk(self, start_dir = os.path.dirname(__file__)):
        for root, dirs, files in os.walk(start_dir):
            contest_id = os.path.split(root)[1]
            if ('conf' in dirs and ('problems' in dirs or 'tests' in dirs)
                               and contest_id.isdigit()
                               and len(contest_id) == 6):
                yield (contest_id.lstrip('0'), root)
