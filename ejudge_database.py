class EjudgeSubmitInfo:
    def __init__(self, problem_id, user_id, lang_id, timestamp):
        self.problem_id = problem_id
        self.user_id = user_id
        self.lang_id = lang_id
        self.timestamp = timestamp


class EjudgeDatabase:
    def __init__(self, ejudge_cursor):
        self.data = {}
        self.db_cursor = ejudge_cursor

    def get_submit_info(self, contest_id, submit_id):
        self.db_cursor.execute('SELECT problem_id,user_id,lang_id,create_time '
                               'FROM runs '
                               'WHERE contest_id=? AND submit_id=?', contest_id, submit_id)
        problem_id, user_id, lang_id, timestamp = list(self.db_cursor.get_row())
        return EjudgeSubmitInfo(problem_id, user_id, lang_id, timestamp)