import configparser
import os
import logging


def parse_args_filters(parser):
    parser.add_argument('--filter-problem', help='process only submits for the problem selected')
    parser.add_argument('--filter-contest', help='process only submits in the selected contest')


def parse_args_input(parser):
    parser.add_argument('--database', help="database file")


def parse_args_output(parser):
    parser.add_argument('-c', '--console', help='output to console', action='store_true')
    parser.add_argument('-o', '--output', help='output file')


def parse_args_config(parser):
    parser.add_argument('--cfg', help="config file")


def init_logging(config):
    try:
        loglevel = config['logging']['level'].upper()
    except Exception:
        loglevel = 'INFO'
    logging.basicConfig(level=getattr(logging, loglevel), format='[%(levelname)s] %(message)s')


def read_config(filename, section=None):
    config = configparser.ConfigParser()
    config.read(filename)
    if section is not None:
        if section in config:
            return config[section]
        else:
            return None
    else:
        return config


def get_contests_from_dir(base_dir):
    return [base_dir + os.path.sep + i for i in os.listdir(base_dir)]
