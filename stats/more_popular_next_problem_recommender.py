from sqlite_connector import SQLiteConnector


class MorePopularNextProblemRecommender:
    def __init__(self, our_db_cursor, pesto_db_cursor):
        self.our_db_cursor = our_db_cursor
        self.pesto_db_cursor = pesto_db_cursor
        self._problem_by_ref = dict()

    def get_recommendation(self, user_id):
        contest_id, problem_id = self._last_problem(user_id)
        self.pesto_db_cursor.execute('SELECT recomended_contest_id, recomended_problem_id '
                                            'FROM more_popular_next_problems_recomendations '
                                            'WHERE contest_id = ? AND problem_id = ?',
                                            (contest_id, problem_id))
        recommendations_row = self.pesto_db_cursor.fetchall()
        recommendations = [tuple(rec) for rec in recommendations_row]
        return recommendations

    def fill_recommendations_table(self):
        self.our_db_cursor.execute('SELECT id FROM users')
        database_users_ids = self.our_db_cursor.fetchall()
        #the number of such sequences is the problem_ref-problem_ref
        number_of_sequences = dict()

        for user_id_row in database_users_ids:
            self.our_db_cursor.execute('SELECT problem_ref '
                                         'FROM submits '
                                         'WHERE user_ref=? AND outcome=? '
                                         'ORDER BY timestamp', (user_id_row['id'], 'OK'))

            sorted_problems_refs = self.our_db_cursor.fetchall()

            for list_id, problem_ref_row in enumerate(sorted_problems_refs[:-1]):
                problem_ref = problem_ref_row['problem_ref']
                next_ref = sorted_problems_refs[list_id + 1]['problem_ref']
                if problem_ref in number_of_sequences:
                    if next_ref in number_of_sequences[problem_ref]:
                        number_of_sequences[problem_ref][next_ref] += 1
                    else:
                        number_of_sequences[problem_ref][next_ref] = 1
                else:
                    number_of_sequences[problem_ref] = {next_ref:1}

        result = dict()
        for problem_ref_start in number_of_sequences:
            for problem_ref_next in number_of_sequences[problem_ref_start]:
                start_contest_problem = self._get_problem_id_by_problem_ref(problem_ref_start)
                next_contest_problem = self._get_problem_id_by_problem_ref(problem_ref_next)

                node = (number_of_sequences[problem_ref_start][problem_ref_next], next_contest_problem)

                if start_contest_problem in result:
                    result[start_contest_problem].append(node)
                else:
                    result[start_contest_problem] = [node]
        self._clear_table()
        for key in result:
            result[key].sort()
            for some in result[key][:min(len(result[key]), 4)]:
                self._write_to_db(key, some[1])

    def _last_problem(self, user_id):
        self.our_db_cursor.execute('SELECT id '
                               'FROM users '
                               'WHERE user_id=?', (user_id, ))

        database_user_id = self.our_db_cursor.fetchone()[0]
        self.our_db_cursor.execute('SELECT problem_ref '
                               'FROM submits '
                               'WHERE user_ref=? '
                               'ORDER BY submits.timestamp DESC '
                                   'LIMIT 1', (database_user_id, ))

        problem_ref = self.our_db_cursor.fetchone()[0]
        return self._get_problem_id_by_problem_ref(problem_ref)

    def _get_problem_id_by_problem_ref(self, problem_ref):
        if problem_ref in self._problem_by_ref:
            problem_id = self._problem_by_ref[problem_ref]
        else:
            self.our_db_cursor.execute('SELECT contests.contest_id,problems.problem_id '
                                         'FROM problems,contests '
                                         'WHERE contest_ref=contests.id AND problems.id=?', (problem_ref, ))
            problem_id = tuple(self.our_db_cursor.fetchone())
            self._problem_by_ref[problem_ref] = problem_id
        return problem_id

    def _clear_table(self):
        self.pesto_db_cursor.execute('DELETE FROM more_popular_next_problems_recomendations')

    def _write_to_db(self, contest_problem, recommended_cont_prob):
        self.pesto_db_cursor.execute('INSERT INTO more_popular_next_problems_recomendations '
                                     '(id,contest_id,problem_id,recomended_contest_id,recomended_problem_id) '
                                     'VALUES (null,?,?,?,?)',
                                     (contest_problem[0], contest_problem[1], recommended_cont_prob[0], recommended_cont_prob[1]))