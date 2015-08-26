from sqlite_connector import SQLiteConnector
import sqlite3
import argparse
import toollib
import logging
import os
from scheme_update_funcs import *


#version in code
ACTUAL_SCHEMA_VERSION = 1


def parse_args():
    parser = argparse.ArgumentParser(description="It updates pesto db schema\n"
                                                 "You need to fill the config file first")
    parser.add_argument('--cfg', help="Config file. By default config.ini is used",
                        default='config.ini')
    parser.add_argument('--log', help="Log filename. By default none file log is used",
                        default=None)

    parser.add_argument('--update_to', help='Version to which you want to update the database. Actual(code) version by default',
                        default=ACTUAL_SCHEMA_VERSION)

    return vars(parser.parse_args())


def get_arguments():
    args = parse_args()
    config = None
    log_filename = args['log']
    config_name = args['cfg']
    try:
        target_schema_version = int(args['update_to'])
    except Exception:
        print('Shema version must be integer')
        exit()

    try:
        config = toollib.read_config(config_name, 'update_db')
    except KeyError:
        print('Incorrect config filename.')
        exit()

    if config is None:
        print('Incorrect config name, try again')
        exit()

    try:
        db_filename = config['db_filename']
    except KeyError:
        print('Wrong config file:Pesto db parameters are not specified')
        exit()



    return args, db_filename, log_filename, target_schema_version


def get_schema_version(db_cursor):
    logging.info('Receiving schema version')
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

    logging.info('Database schema version is {}'.format(schema_version))

    return schema_version


def start_update(connector, target_schema_version):
    db_cursor = connector.get_cursor()
    schema_version = get_schema_version(db_cursor)

    logging.info('Starting update from {} to {}'.format(schema_version, target_schema_version))

    while schema_version != target_schema_version:
        try:
            update_func = globals()['update_from_v{}_to_v{}'.format(schema_version, schema_version + 1)]
        except KeyError:
            logging.error('Undefined transition from version {} to {}'.format(schema_version, schema_version + 1))
            return
        logging.info('transition from version {} to {} ..'.format(schema_version, schema_version + 1))
        try:
            update_func(db_cursor)
        except Exception as e:
            logging.error('transition faild: ' + str(e))
            return
        else:
            logging.info('transition from {} to {} successful. Commiting changes.'.format(schema_version, schema_version + 1))
            connector.sqlite_connection.commit()
            logging.info('Changes commited')
            schema_version += 1

    logging.info('Update successful')

def main():
    args, db_filename, log_filename, target_schema_version = get_arguments()

    if log_filename:
        logging.basicConfig(filename=log_filename, format='[%(asctime)s]  %(levelname)s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='[%(asctime)s]  %(levelname)s: %(message)s', level=logging.INFO)

    if os.path.isfile(db_filename):
        pesto_connector = SQLiteConnector()
        pesto_connector.create_connection(db_filename)
        logging.info('Connected to Pesto database')
    else:
        logging.error('Input database file not found')
        exit()

    start_update(pesto_connector, target_schema_version)

    logging.info('Closing connection..')
    pesto_connector.close_connection()
    logging.info('Connection closed')

if __name__ == "__main__":
    main()