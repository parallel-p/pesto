#!/usr/bin/python3

import sqlite3
import argparse
import toollib
import logging
from extract_cases_to_db import extract_cases_to_db
from walker import MultipleContestWalker
from fill_db_from_contest_xml import fill_db_from_contest_xml
from mysql_connector import MySQLConnector
from fill_database import fill_from_xml, fill_from_pickles
import sys
from traceback import print_exception

def parse_args():
    parser = argparse.ArgumentParser(description="Dump all the data to the database\n"
                                                 "You need to fill the config file first")
    parser.add_argument('--cfg', help="config file. By default config.ini is used",
                        default='config.ini')
    parser.add_argument('-p', help='Use pickle database. '
                                   'By default MySQL and xml databases are used',
                        action='store_true')
    parser.add_argument('--clean', help='Create new or overwrite existing database',
                        action='store_true')
    parser.add_argument('--hashes-only', help='Fill cases i/o hashes only',
                        action='store_true')
    parser.add_argument('--no-hashes', help='Do not fill cases i/o hashes',
                        action='store_true')
    parser.add_argument('--update', help='Update an existing database. Used by default',
                        action='store_true')
    parser.add_argument('--start-from', help='Number of contest to start filling cases from',
                        default='1')
    parser.add_argument('--contests-names', help='Fill in contests names only',
                        action='store_true')
    return vars(parser.parse_args())


def get_arguments():
    args = parse_args()
    config = None

    config_name = args['cfg']
    try:
        config = toollib.read_config(config_name, 'db_tool')
    except KeyError:
        print('Incorrect config filename.')
        exit()
    if config is None:
        print('Incorrect config name, try again')
        exit()

    base_dir = config['base_dir']
    pickle_dir = config['pickle_dir']
    output_database = config['output_database']
    origin = config['origin']
    contests_info_dir = config['contests_info_dir']
    if origin == '':
        print('Origin is not specified')
        exit()

    try:
        mysql_config = {
            'user': config['mysql_user'],
            'password': config['mysql_password'],
            'host': config['mysql_host'],
            'port': config['mysql_port'],
            'database': config['mysql_db_name']
        }
    except KeyError:
        print('Wrong config file: MySQL parameters are not specified')
        exit()
    try:
        loglevel = toollib.read_config(config_name, 'logging')['level'].upper()
        toollib.init_logging(loglevel)
    except Exception:
        pass
    return base_dir, args, pickle_dir, output_database, origin, mysql_config, contests_info_dir


def create_tables(cursor, filename):
    script_file = open(filename)
    script = script_file.read()
    cursor.executescript(script)


def create_new_database(path, tables_script_filename):
    db_file = open(path, 'w')
    db_file.close()
    connection = sqlite3.connect(path)
    create_tables(connection.cursor(), tables_script_filename)
    return connection, connection.cursor()


def update_database(path):
    connection = sqlite3.connect(path)
    tables = list(connection.execute("SELECT name FROM sqlite_master WHERE type='table'"))
    if tables == []:
        logging.error("Database is empty, can't update it")
        exit()
    return connection, connection.cursor()


def fill_cases_hashes(cursor, base_dir, origin, startfrom):
    startfrom = startfrom
    logging.info("Filling cases starting from contest #{}".format(startfrom))
    extract_cases_to_db(MultipleContestWalker().walk(base_dir, path_only=True), cursor,
                        origin, startfrom)


def fill_submits(sqlite_cursor, base_dir, origin, mysql_config):
    if '' in mysql_config.values():
        logging.error('MySQL parameters are not specified')
        exit()
    logging.info('Now connecting to MySQL')
    mysql_connector = MySQLConnector()
    mysql_connector.create_connection(mysql_config)
    logging.info('Connected to MySQL database')
    ej_cursor = mysql_connector.get_cursor()
    logging.info("Filling database from XML's and MySQL database")
    fill_from_xml(sqlite_cursor, ej_cursor, base_dir, origin)
    mysql_connector.close()

def fill_contests_names(sqlite_cursor, contests_info_dir, origin):
    if contests_info_dir:
        logging.info('Filling contests names')
        fill_db_from_contest_xml(contests_info_dir, sqlite_cursor, origin)
        logging.info('Contests names were filled')

def main():
    base_dir, args, pickle_dir, output_database, origin, mysql_config, contests_info_dir = get_arguments()

    if args['clean']:
        connection, sqlite_cursor = create_new_database(output_database, 'tables_script.txt')
        logging.info("Database created successfully")
    else:
        connection, sqlite_cursor = update_database(output_database)
        logging.info("Database is going to be updated")

    if not contests_info_dir:
        logging.warning("Contests info directory is not specified. Contests name won't be filled")
    try:
        if args['contests_names']:
            fill_contests_names(sqlite_cursor, contests_info_dir, origin)
            connection.commit()
            connection.close()
            exit()
        if args['hashes_only']:
            fill_cases_hashes(sqlite_cursor, base_dir, origin, args['start_from'])
            connection.commit()
            connection.close()
            logging.info('Case hashes were filled successfully')
            logging.info('Connection closed')
            exit()
        if args['p']:
            logging.info('Filling database from pickles...')
            fill_from_pickles(sqlite_cursor, pickle_dir, origin)
            connection.commit()
        else:
            fill_submits(sqlite_cursor, base_dir, origin, mysql_config)
            connection.commit()

        if not args['no_hashes']:
            fill_cases_hashes(sqlite_cursor, base_dir, origin, args['start_from'])

        fill_contests_names(sqlite_cursor, contests_info_dir, origin)

    except Exception:
        logging.exception('Exception caught')
        connection.commit()
        connection.close()
        logging.info('Connection closed')
        exit()

    connection.commit()
    connection.close()
    logging.info('Connection closed')


if __name__ == "__main__":
    main()
