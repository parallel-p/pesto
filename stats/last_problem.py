def last_problem(user_id, db_cursor):
    db_cursor.execute('SELECT FIRST 1 problems.problem_id, contests.contest_id'
                      'FROM problems, users, submits'
                      'WHERE user_id=? '
                      'ORDER_BY submits.timestamp', user_id)
    return tuple(db_cursor.fetchone())