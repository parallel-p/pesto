def _update_scheme_version(db_cursor, new_version):
    db_cursor.execute('UPDATE Configuration '
                      'SET version_of_the_database_schema = ?', (new_version, ))


def update_from_v0_to_v1(db_cursor):
    db_cursor.execute('CREATE TABLE Configuration(version_of_the_database_schema, INTEGER)')
    db_cursor.execute('INSERT INTO Configuration '
                      '(version_of_the_database_schema) '
                      'VALUES (?)', (0, ))
    _update_scheme_version(db_cursor, 1)

