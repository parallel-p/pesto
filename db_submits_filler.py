class DBSubmitsFiller:
    def __init__(self, db_cur):
        self.db_cur = db_cur

    def fill_db_from_submit(self, submit, origin):
        submit.problem_id[0] = submit.problem_id[0].rjust(6, '0')
        contest_def = [('origin', origin), ('scoring', submit.scoring), ('contest_id', submit.problem_id[0])]
        contest_ref = self.db_define_ref('Contests', contest_def)

        user_def = [('origin', origin), ('user_id', submit.user_id)]
        user_ref = self.db_define_ref('Users', user_def)

        problem_def = [('contest_ref', contest_ref), ('problem_id', submit.problem_id[1])]
        problem_ref = self.db_define_ref('Problems', problem_def)

        submit_def = [('submit_id', submit.submit_id), ('problem', problem_ref)]
        submit_ref = self.db_define_ref('Submits', submit_def)

        update = [('lang_id', submit.lang_id), ('outcome', submit.outcome), ('timestamp', submit.timestamp),
                  ('user_ref', user_ref)]
        self.db_update('Submits', submit_ref, update)

        for run in submit.runs:
            case_def = [('problem_ref', problem_ref), ('case_id', run.case_id)]
            case_ref = self.db_define_ref('Cases', case_def)

            run_def = [('submit_ref', submit_ref), ('case_ref', case_ref)]
            run_ref = self.db_define_ref('Runs', run_def)

            update = [('realtime', run.real_time), ('time', run.time), ('outcome', run.outcome)]
            self.db_update('Runs', run_ref, update)

    def db_define_ref(self, table_name, params):
        ref = self.db_find_ref(table_name, params)
        if ref is None:
            self.db_cur.execute('INSERT INTO ' + table_name + ' (id' + ', ?' * len(params) + ') VALUES (NULL' +
                                ', ?' * len(params) + ')', *[y for x in zip(*params) for y in x])
            ref = self.db_find_ref(table_name, params)
        return ref

    def db_find_ref(self, table_name, params):
        self.db_cur.execute('SELECT id FROM ' + table_name + ' WHERE ' + ' AND '.join(['? = ?'] * len(params)),
                            *[y for x in params for y in x])
        query = self.db_cur.fetchone()
        return query[0] if query else None

    def db_update(self, table_name, ref, update):
        self.db_cur.execute('UPDATE ' + table_name + ' SET ' + ', '.join(['? = ?'] * len(update)) + ' WHERE id = ?',
                            *([y for x in update for y in x] + [ref]))
