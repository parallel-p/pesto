class MorePopularNextProblemRecommender:
    def __init__(self, our_db_cursor, pesto_db_cursor):
        self.our_db_cursor = our_db_cursor
        self.pesto_db_cursor = pesto_db_cursor

    def _last_problem(self, user_id):
        self.pesto_db_cursor.execute('SELECT id '
                               'FROM users '
                               'WHERE user_id=?', user_id)

        database_user_id = self.pesto_db_cursor.fetchone()[0]
        self.pesto_db_cursor.execute('SELECT FIRST 1 contest_ref,problem_ref '
                               'FROM submits '
                               'WHERE user_ref=? '
                               'ORDER BY submits.timestamp DESC', database_user_id)

        database_contest_problem_id = self.pesto_db_cursor.fetchone()

        self.pesto_db_cursor.execute('SELECT contest_id,problem_id '
                               'FROM contests,problems '
                               'WHERE contests.id=? AND problems.id=?', database_contest_problem_id[0], database_contest_problem_id[1])

        contest_problem_id = self.our_db_cursor.fetchone()
        return tuple(contest_problem_id)

    def get_recommendation(self, user_id):
        contest_id, problem_id = self._last_problem(user_id)
        self.pesto_db_cursor.execute('SELECT recomended_contest_id, recomended_problem_id '
                                            'FROM more_popular_next_problems_recomendations '
                                            'WHERE contest_id = "?" AND problem_id = "?"',
                                            (contest_id, problem_id))
        recommendations = self.pesto_db_cursor.fetchone()
        return recommendations

    def fill_recommendations_table(self):
        pass