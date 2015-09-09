import sqlite3
import logging
from extract_cases_to_db import extract_cases_to_db
from walker import MultipleContestWalker
from fill_db_from_contest_xml import fill_db_from_contest_xml
from mysql_connector import MySQLConnector
from fill_database import fill_from_xml


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

def fill_database(output_database, base_dir, contests_info_dir, mysql_config, origin, extra):
    if 'clean' in extra:
        connection, sqlite_cursor = create_new_database(output_database, 'tables_script.txt')
        logging.info("Database created successfully")
    else:
        connection, sqlite_cursor = update_database(output_database)
        logging.info("Database is going to be updated")

    if not contests_info_dir:
        logging.warning("Contests info directory is not specified. Contests name won't be filled")
    try:
        if 'contests_names' in extra:
            fill_contests_names(sqlite_cursor, contests_info_dir, origin)
            connection.commit()
            connection.close()
            exit()
        if 'hashes_only' in extra:
            fill_cases_hashes(sqlite_cursor, base_dir, origin, extra['start_from'])
            connection.commit()
            connection.close()
            logging.info('Case hashes were filled successfully')
            logging.info('Connection closed')
            exit()
        fill_submits(sqlite_cursor, base_dir, origin, mysql_config)
        connection.commit()

        if 'no_hashes' not in extra:
            fill_cases_hashes(sqlite_cursor, base_dir, origin, extra['start_from'])

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
