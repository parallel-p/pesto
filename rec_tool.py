from stats.more_popular_next_problem_recommender import MorePopularNextProblemRecommender
import argparse
import toollib
from mysql_connector import MySQLConnector
from sqlite_connector import SQLiteConnector
import sys
from traceback import print_exception
import logging
import os.path


def parse_args():
    parser = argparse.ArgumentParser(description="It fill`s recommendations table\n"
                                                 "You need to fill the config file first")
    parser.add_argument('--cfg', help="config file. By default config.ini is used",
                        default='config.ini')
    parser.add_argument('--log', help="log filename. By default none file log is used",
                        default=None)
    parser.add_argument('--start-from', help='Number of user to start recommendations generate from',
                        default='')
    parser.add_argument('--end', help='Number of user to end recommendations generate',
                        default='')
    return vars(parser.parse_args())


def get_arguments():
    args = parse_args()
    config = None
    log_filename = args['log']
    config_name = args['cfg']
    if not config_name:
        config_name = 'config.ini'
    try:
        config = toollib.read_config(config_name, 'recommender_tool')
    except KeyError:
        print('Incorrect config filename.')
        exit()
    if config is None:
        print('Incorrect config name, try again')
        exit()

    try:
        input_sqlite_db_filename = config['input_db_filename']
    except KeyError:
        print('Wrong config file:Pesto SQLite db parameters are not specified')
        exit()

    try:
        output_mysql_db_config = {
            'user': config['output_db_user'],
            'password': config['output_db_password'],
            'host': config['output_db_host'],
            'port': config['output_db_port'],
            'database': config['output_db_name']
        }
    except KeyError:
        print('Wrong config file:Output DB MySQL parameters are not specified')
        exit()

    return args, input_sqlite_db_filename, output_mysql_db_config, log_filename

def get_mysql_connector(mysql_config):
    if '' in mysql_config.values():
        logging.info('MySQL parameters are not specified')
        exit()
    logging.info('Now connecting to MySQL')
    mysql_connector = MySQLConnector()
    mysql_connector.create_connection(mysql_config)
    logging.info('Connected to MySQL database')
    return mysql_connector


def main():
    args, input_db_config, output_db_config, log_filename = get_arguments()

    if log_filename:
        logging.basicConfig(filename=log_filename, format='[%(asctime)s]  %(levelname)s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='[%(asctime)s]  %(levelname)s: %(message)s', level=logging.INFO)

    if os.path.isfile(input_db_config):
        pesto_connector = SQLiteConnector()
        pesto_connector.create_connection(input_db_config)
        logging.info('Connected to Pesto database')
    else:
        logging.error('Input database file not found')
        exit()
    output_connector = get_mysql_connector(output_db_config)

    try:
        pesto_cur = pesto_connector.get_cursor()
        informatics_cur = output_connector.get_cursor()
        recommender = MorePopularNextProblemRecommender(pesto_cur, informatics_cur)
        if args['start_from']:
            between = (args['start_from'], args['end'])
            recommender.fill_recommendations_table(between)
        else:
            recommender.fill_recommendations_table()

    except SystemExit:
        raise
    except:
        logging.critical('The following exception was caught:')
        print_exception(*sys.exc_info())
        pesto_connector.close_connection()
        logging.info('Pesto connection closed')
        output_connector.connection.commit()
        output_connector.close()
        logging.info('Output connection closed')
        exit()

    pesto_connector.close_connection
    logging.info('Pesto connection closed')
    output_connector.connection.commit()
    output_connector.close()
    logging.info('Output connection closed')
    logging.info('Connection closed')


if __name__ == "__main__":
    main()
