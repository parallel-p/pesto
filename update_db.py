import sqlite3
import logging
import scheme_update_funcs


def get_schema_version(db_cursor):
    schema_version = 0
    try:
        db_cursor.execute('SELECT version_of_the_database_schema FROM Configuration')
        schema_version = db_cursor.fetchone()
        if not schema_version:
            logging.error('Configuration is empty')
            exit()
        schema_version = schema_version['version_of_the_database_schema']
    except sqlite3.OperationalError:
        logging.error('Not found configuration table or version column in configuration table')

    logging.debug('Database schema version is {}'.format(schema_version))

    return schema_version


def start_update(connector, target_schema_version):
    db_cursor = connector.get_cursor()
    schema_version = get_schema_version(db_cursor)
    if schema_version > target_schema_version:
        logging.fatal('Database version {} is not supported'.format(schema_version))
        exit()

    while schema_version < target_schema_version:
        update_func_name = 'update_from_v{}_to_v{}'.format(schema_version, schema_version + 1)
        try:
            update_func = getattr(scheme_update_funcs, update_func_name)
        except AttributeError:
            logging.error('Undefined transition from version {} to {}'.format(schema_version, schema_version + 1))
            return
        logging.info('transition from version {} to {} ..'.format(schema_version, schema_version + 1))
        try:
            update_func(db_cursor)
        except Exception as e:
            logging.error('transition faild: ' + str(e))
            return
        else:
            logging.info(
                'transition from {} to {} successful. Commiting changes.'.format(schema_version, schema_version + 1))
            connector.sqlite_connection.commit()
            logging.info('Changes commited')
            schema_version += 1

