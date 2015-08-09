import ejudge_contest
import model
import md5_hasher
import walker


def problem_generator(contest_dirs):
    for contest_id, contest_dir in contest_dirs:
        for problem in walker.ProblemWalker().walk(contest_dir):
            yield problem

