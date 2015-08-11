import sqlite3
import argparse
import toollib
from extract_cases_to_db import extract_cases_to_db
from walker import MultipleContestWalker
from fill_db_from_contest_xml import fill_db_from_contest_xml
from mysql_connector import MySQLConnector
from fill_database import fill_from_xml, fill_from_pickles


def create_tables(cursor, filename):
    script_file = open(filename)
    script = script_file.read()
    cursor.executescript(script)


def parse_args():
    parser = argparse.ArgumentParser(description="Dump all the data to the database\n"
                                                 "You need to fill the config file first")
    parser.add_argument('--cfg', help="config file")
    parser.add_argument('-p', help='Use pickle database. '
                                   'By default MySQL and xml databases are used',
                        action='store_true')

    return vars(parser.parse_args())


def get_arguments():
    args = parse_args()
    config = None
    if not args['cfg']:
        print('Config file is not specified')
        exit()
    try:
        config = toollib.read_config(args['cfg'], 'db_tool')
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
    return base_dir, args['p'], pickle_dir, output_database, origin, mysql_config, contests_info_dir

def create_database(path):
    db_file = open(path, 'w')
    db_file.close()
    connection = sqlite3.connect(path)
    return connection.cursor()

def main():
    base_dir, is_pickle, pickle_dir, output_database, origin, mysql_config, contests_info_dir = get_arguments()
    db_file = open(output_database, 'w')
    db_file.close()

    connection = sqlite3.connect(output_database)
    sqlite_cursor = connection.cursor()

    create_tables(sqlite_cursor, 'tables_script.txt')
    print("Database created successfully")
    # except OperationalError:
    #     print(OperationalError)
    contests_dir = [c_dir[1] for c_dir in MultipleContestWalker().walk(base_dir)]
    if contests_info_dir == '':
        print("WARNING. Contests info directory is not specified. Contests name won't be filled")
    if is_pickle:
        print('Filling database from pickles...')
        fill_from_pickles(sqlite_cursor, pickle_dir, origin)
        connection.commit()
    else:
        if '' in mysql_config.values():
            print('MySQL parameters are not specified')
            exit()
        print('Now connecting to MySQL')
        mysql_connector = MySQLConnector()
        mysql_connector.create_connection(mysql_config)
        print('Connected to MySQL database')
        ej_cursor = mysql_connector.get_cursor()
        print("Filling database from XML's and MySQL database")
        fill_from_xml(sqlite_cursor, ej_cursor, base_dir, origin)
        mysql_connector.close()
        connection.commit()
    extract_cases_to_db(contests_dir, sqlite_cursor, origin)
    if contests_info_dir != '':
        fill_db_from_contest_xml(contests_info_dir, sqlite_cursor, origin)
    print('Cases were written')
    connection.commit()
    connection.close()
    print('Connection closed')


if __name__ == "__main__":
    main()
