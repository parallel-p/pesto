import logging


class MorePopularNextProblemRecommender:
    def __init__(self, our_db_cursor, stats_db_cursor):
        self.our_db_cursor = our_db_cursor
        self.stats_db_cursor = stats_db_cursor
        self._problem_by_ref = dict()

    def fill_recommendations_table(self, limit=False):
        processing = 0
        log = 0
        if limit:
            self.our_db_cursor.execute('SELECT id FROM users WHERE id > ? AND id < ?', (limit[0], limit[1]))
        else:
            self.our_db_cursor.execute('SELECT id FROM users')
        logging.info('Loading users ids')
        database_users_ids = self.our_db_cursor.fetchall()
        users_num = len(database_users_ids)
        logging.info('Loaded {} users ids'.format(users_num))
        #the number of such sequences is the problem_ref-problem_ref
        number_of_sequences = dict()
        logging.info('Users pocessing')
        for user_id_row in database_users_ids:
            processing += 1
            if processing >= 100:
                log += 1
                processing = 0
                logging.info(' Processed {} from {}'.format(log * 100, users_num))
            self.our_db_cursor.execute('SELECT problem_ref '
                                         'FROM submits '
                                         'WHERE user_ref=? AND outcome=? '
                                         'ORDER BY timestamp', (user_id_row['id'], 'OK'))

            sorted_problems_refs = self.our_db_cursor.fetchall()

            for list_id, problem_ref_row in enumerate(sorted_problems_refs[:-1]):
                problem_ref = problem_ref_row['problem_ref']
                next_ref = sorted_problems_refs[list_id + 1]['problem_ref']
                if problem_ref in number_of_sequences:
                    if next_ref not in number_of_sequences[problem_ref]:
                        number_of_sequences[problem_ref][next_ref] = 0
                    number_of_sequences[problem_ref][next_ref] += 1
                else:
                    number_of_sequences[problem_ref] = {next_ref:1}
        logging.info('Processed {} from {}'.format(log * 100 + processing, users_num))
        result = dict()
        logging.info('Data processing')
        for problem_ref_start in number_of_sequences:
            for problem_ref_next in number_of_sequences[problem_ref_start]:
                start_contest_problem = self._get_problem_id_by_problem_ref(problem_ref_start)
                next_contest_problem = self._get_problem_id_by_problem_ref(problem_ref_next)

                node = (number_of_sequences[problem_ref_start][problem_ref_next], next_contest_problem)

                if start_contest_problem in result:
                    result[start_contest_problem].append(node)
                else:
                    result[start_contest_problem] = [node]

        logging.info('Writing in database')
        for key in result:
            result[key].sort()
            for some in result[key][:min(len(result[key]), 10)]:
                continue
                self._write_to_db(key, some[1])

    def _get_problem_id_by_problem_ref(self, problem_ref):
        if problem_ref in self._problem_by_ref:
            problem_id = self._problem_by_ref[problem_ref]
        else:
            self.our_db_cursor.execute('SELECT Contests.contest_id, Problems.problem_id '
                                         'FROM problems, contests '
                                         'WHERE contest_ref=Contests.id AND Problems.id=?', (problem_ref, ))
            problem_id = tuple(self.our_db_cursor.fetchone())
            self._problem_by_ref[problem_ref] = problem_id
        return problem_id

    def _clear_table(self):
        self.stats_db_cursor.execute('DELETE FROM sis_most_popular_next_problems_recommendations')

    def _write_to_db(self, contest_problem, recommended_cont_prob):
        self.stats_db_cursor.execute('INSERT INTO sis_most_popular_next_problems_recommendations '
                                     '(id,contest_id,problem_id,recommended_contest_id,recommended_problem_id) '
                                     'VALUES (null,%s,%s,%s,%s)',
                                     (contest_problem[0], contest_problem[1], recommended_cont_prob[0], recommended_cont_prob[1]))