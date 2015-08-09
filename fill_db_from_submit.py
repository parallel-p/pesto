def fill_db_from_submit(db_cur, submit, origin):
    contest_def = {'origin': origin, 'scoring': submit.scoring, 'contest_id': submit.problem_id[0]}
    contest_ref = db_define_ref(db_cur, 'Contests', contest_def)

    user_def = {'origin': origin, 'user_id': submit.user_id}
    user_ref = db_define_ref(db_cur, 'Users', user_def)

    problem_def = {'contest_ref': contest_ref, 'problem_id': submit.problem_id[1]}
    problem_ref = db_define_ref(db_cur, 'Problems', problem_def)

    submit_def = {'submit_id': submit.submit_id, 'problem': problem_ref}
    submit_ref = db_define_ref(db_cur, 'Submits', submit_def)

    update = {'lang_id': submit.lang_id, 'outcome': submit.outcome, 'timestamp': submit.timestamp, 'user_ref': user_ref}
    db_update(db_cur, 'Submits', submit_ref, update)

    for run in submit.runs:
        case_def = {'problem_ref': problem_ref, 'case_id': run.case_id}
        case_ref = db_define_ref(db_cur, 'Cases', case_def)

        run_def = {'submit_ref': submit_ref, 'case_ref': case_ref}
        run_ref = db_define_ref(db_cur, 'Runs', run_def)

        update = {'realtime': run.real_time, 'time': run.time, 'outcome': run.outcome}
        db_update(db_cur, 'Runs', run_ref, update)


def db_define_ref(db_cur, table_name, params):
    ref = db_find_ref(db_cur, table_name, params)
    if ref is None:
        db_cur.execute('INSERT INTO ' + table_name + ' (id, ' + ', ?' * len(params) + ') VALUES (NULL' +
                       ', ?' * len(params) + ')', *[y for x in zip(*params.items()) for y in x])
        ref = db_find_ref(db_cur, table_name, params)
    return ref


def db_find_ref(db_cur, table_name, params):
    db_cur.execute('SELECT id FROM ' + table_name + ' WHERE ' + ' AND '.join(['? = ?'] * len(params)),
                   *[y for x in params.items() for y in x])
    query = db_cur.fetchone()
    return query[0] if query else None


def db_update(db_cur, table_name, ref, update):
    db_cur.execute('UPDATE ' + table_name + ' SET ' + ', '.join(['? = ?'] * len(update)) + ' WHERE id = ?',
                   *([y for x in update.items() for y in x] + [ref]))
