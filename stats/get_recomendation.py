from stats.last_problem import last_problem


def get_recomendation(user_id, our_db_cursor, pesto_db_cursor):
    contest_id, problem_id = last_problem(user_id, our_db_cursor)
    recomendations = pesto_db_cursor.execute('SELECT recomended_contest_id, recomended_problem_id '
                                            'FROM more_popular_next_problems_recomendations '
                                            'WHERE contest_id = "?" AND problem_id = "?"',
                                            (contest_id, problem_id)).fetchall()
    return recomendations
