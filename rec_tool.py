from stats.more_popular_next_problem_recommender import MorePopularNextProblemRecommender
import argparse
import toollib
from mysql_connector import MySQLConnector
import sys
from traceback import print_exception

def parse_args():
    parser = argparse.ArgumentParser(description="It fill`s recommendations table\n"
                                                 "You need to fill the config file first")
    parser.add_argument('--cfg', help="config file. By default config.ini is used",
                        default='config.ini')
    parser.add_argument('--start-from', help='Number of user to start recommendations generate from',
                        default='')
    parser.add_argument('--end', help='Number of user to end recommendations generate',
                        default='')
    return vars(parser.parse_args())


def get_arguments():
    args = parse_args()
    config = None

    config_name = args['cfg']
    try:
        config = toollib.read_config(config_name, 'recommender_tool')
    except KeyError:
        print('Incorrect config filename.')
        exit()
    if config is None:
        print('Incorrect config name, try again')
        exit()

    try:
        pesto_mysql_config = {
            'user': config['pesto_user'],
            'password': config['pesto_password'],
            'host': config['pesto_host'],
            'port': config['pesto_port'],
            'database': config['pesto_db_name']
        }
    except KeyError:
        print('Wrong config file:Pesto MySQL parameters are not specified')
        exit()

    try:
        informatics_mysql_config = {
            'user': config['informatics_user'],
            'password': config['informatics_password'],
            'host': config['informatics_host'],
            'port': config['informatics_port'],
            'database': config['informatics_db_name']
        }
    except KeyError:
        print('Wrong config file:Informatics MySQL parameters are not specified')
        exit()

    return args, pesto_mysql_config, informatics_mysql_config

def get_mysql_connector(mysql_config):
    if '' in mysql_config.values():
        print('MySQL parameters are not specified')
        exit()
    print('Now connecting to MySQL')
    mysql_connector = MySQLConnector()
    mysql_connector.create_connection(mysql_config)
    print('Connected to MySQL database')
    return mysql_connector


def main():
    args, pesto_config, infromatics_config = get_arguments()
    pesto_connector = get_mysql_connector(pesto_config)
    informatics_connector = get_mysql_connector(infromatics_config)

    try:
        pesto_cur = pesto_connector.get_cursor()
        informatics_cur = informatics_connector.get_cursor()
        recommender = MorePopularNextProblemRecommender(informatics_cur, pesto_cur)
        if args['start_from']:
            between = (args['start_from'], args['end'])
            recommender.fill_recommendations_table(between)
        else:
            recommender.fill_recommendations_table()

    except SystemExit:
        raise
    except:
        print('The following exception was caught:')
        print_exception(*sys.exc_info())
        pesto_connector.connection.commit()
        pesto_connector.connection.close()
        print('Pesto connection closed')
        informatics_connector.close()
        exit()

    pesto_connector.connectionconnection.commit()
    pesto_connector.close()
    informatics_connector.close()
    print('Connection closed')


if __name__ == "__main__":
    main()
