import logging


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
        query = ('SELECT prob_id,user_id,lang_id,create_time '
                 'FROM ejudge.runs '
                 'WHERE contest_id=%(contest)s AND run_id=%(submit)s')
        self.db_cursor.execute(query, {'contest': contest_id, 'submit': submit_id})
        response = self.db_cursor.fetchone()
        if response is None:
            logging.warning('Submit {} from contest {} not found in database'.format(submit_id, contest_id))
            return None
        problem_id, user_id, lang_id, timestamp = list(response)
        return EjudgeSubmitInfo(problem_id, user_id, lang_id, timestamp)
