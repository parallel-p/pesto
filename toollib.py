import configparser


def parse_args_filters(parser):
    parser.add_argument('--filter-problem', help='process only submits for the problem selected')
    parser.add_argument('--filter-user', help='process only submits by the selected user')
    parser.add_argument('--filter-contest', help='process only submits in the selected contest')

def parse_args_input(parser):
    parser.add_argument('-m', '--multicontest', help='base_dir contains several contests', action='store_true')
    parser.add_argument('--dir', help="directory containing xml's/pickles")

def parse_args_output(parser):
    parser.add_argument('-c', '--console', help='output to console', action='store_true')
    parser.add_argument('-o', '--outfile', help='output file')

def parse_args_config(parser):
    parser.add_argument('--cfg', help="config file")

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
    home_dirs = [base_dir + os.path.sep + i for i in os.listdir(base_dir)]