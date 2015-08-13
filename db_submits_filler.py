class DBSubmitsFiller:
    def __init__(self, db_cur):
        self.db_cur = db_cur

    def fill_db_from_submit(self, submit, origin):
        submit.problem_id = [submit.problem_id[0].rjust(6, '0'), submit.problem_id[1]]

        keys, values = ['origin', 'scoring', 'contest_id'], [origin, submit.scoring, submit.problem_id[0]]
        contest_ref = self.db_define_ref('Contests', keys, values)

        keys, values = ['origin', 'user_id'], [origin, submit.user_id]
        user_ref = self.db_define_ref('Users', keys, values)

        keys, values = ['contest_ref', 'problem_id'], [contest_ref, submit.problem_id[1]]
        problem_ref = self.db_define_ref('Problems', keys, values)

        keys, values = ['submit_id', 'problem_ref'], [submit.submit_id, problem_ref]
        submit_ref = self.db_define_ref('Submits', keys, values)

        keys = ['lang_id', 'outcome', 'timestamp', 'user_ref']
        values = [submit.lang_id, submit.outcome, submit.timestamp, user_ref]
        self.db_update('Submits', submit_ref, keys, values)

        for run in submit.runs:
            keys, values = ['problem_ref', 'case_id'], [problem_ref, run.case_id]
            case_ref = self.db_define_ref('Cases', keys, values)

            keys, values = ['submit_ref', 'case_ref'], [submit_ref, case_ref]
            run_ref = self.db_define_ref('Runs', keys, values)

            keys, values = ['realtime', 'time', 'outcome'], [run.real_time, run.time, run.outcome]
            self.db_update('Runs', run_ref, keys, values)

    def db_define_ref(self, table, keys, values):
        ref = self.db_find_ref(table, keys, values)
        if ref is None:
            keys_str = ', '.join(keys)
            ans = ', ?' * len(keys)
            self.db_cur.execute('INSERT INTO {} (id, {}) VALUES (NULL{})'.format(table, keys_str, ans), values)
            ref = self.db_cur.lastrowid
        return ref

    def db_find_ref(self, table, keys, values):
        equals = ' AND '.join(['{} = ?'] * len(keys)).format(*keys)
        self.db_cur.execute('SELECT id FROM {} WHERE {}'.format(table, equals), values)
        query = self.db_cur.fetchone()
        return query[0] if query else None

    def db_update(self, table, ref, keys, values):
        equals = ', '.join(['{} = ?'] * len(keys)).format(*keys)
        self.db_cur.execute('UPDATE {} SET {} WHERE id = {}'.format(table, equals, ref), values)
