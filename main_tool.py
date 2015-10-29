#!/usr/bin/python3

import toollib
import tool_config
from argparse import ArgumentParser
import db_tool
from  sqlite_connector import SQLiteConnector
import update_db
import os.path


SCHEMA_VERSION = 3


def die(message):
    print(message)
    exit()

def parse_args():
    parser = ArgumentParser(description="Pesto - someone will add some description here later")

    parser.add_argument('--cfg', help="config file")
    parser.add_argument('--database', help="database file")
    parser.add_argument('-c', '--console', help='output to console', action='store_true')
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('action', help='action to perform (stat, fill)')  # TODO all actions

    # tool
    parser.add_argument('-p', '--problem', help='process only submits for the problem selected (contest:problem)')
    parser.add_argument('-s', '--scoring', help="contest scoring (acm, kirov)")
    parser.add_argument('--lang-sharding', help="shard by language in submits_by_signature",
                        action="store_true")
    parser.add_argument('--min-submits', help="minimal submits count for submits_by_signature")
    parser.add_argument('--pretty-json', help="prettify build_tree output",
                        action="store_true")
    parser.add_argument('preset', help="name or number of statistics preset", nargs='?')

    # run_cases_stats
    parser.add_argument('--tree-json', help="saved tree (only for draw_saved_tree)")

    # db_tool
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
    config_name = args['cfg'] or 'config.ini'
    action = args['action']
    if action not in ['stat', 'fill']:
        die('Invalid action')
    try:
        config = toollib.read_config(config_name)
        toollib.init_logging(config)
        config['global']  # ensure that this section exists
    except Exception:
        die('Unable to parse config file')
    if config is None:
        die('Unable to parse config file')
    config = dict(config)
    database_name = args['database'] or config['global'].get('database') or die('Database not found')
    database_name = os.path.expanduser(database_name)

    if action == 'stat':
        if args['console']:
            outfile = None
        elif args['output']:
            outfile = args['output']
        elif config['global'].get('output'):
            outfile = config['global']['output']
        else:
            outfile = None
    else:
        outfile = None
    if outfile:
        outfile = os.path.expanduser(outfile)

    filters = {}
    if args['problem']:
        if args['problem'].count(':') != 1:
            die('Problem filter should be specified as CONTEST:PROBLEM. You can also write CONTEST: or :PROBLEM.')
        cf, pf = args['problem'].split(':')
        if cf:
            filters['contest'] = cf.rjust(6, '0')
        if pf:
            if pf.isdigit():
                filters['problem'] = pf
            elif pf.isalpha():
                # a = 1, z = 26, aa = 27 and so on
                val = 0
                for i in pf.upper():
                    val *= 26
                    val += ord(i) - ord('A') + 1
                filters['problem'] = str(val)
    if args['scoring']:
        filters['scoring'] = args['scoring'].upper()
    elif config.get('stat', {}).get('scoring'):
        filters['scoring'] = config['stat']['scoring'].upper()
    if 'scoring' in filters and filters['scoring'] == 'ALL':
        del filters['scoring']

    extra = {}
    extra['min_submits'] = 0
    if config.get('submits_by_signature', {}).get('min_submits') is not None:
        extra['min_submits'] = int(config['submits_by_signature']['min_submits'])
    if args['lang_sharding']:
        extra['lang_sharding'] = True
    if args['min_submits']:
        extra['min_submits'] = int(args['min_submits'])
    if args['pretty_json']:
        extra['pretty_json'] = True
    if args['tree_json']:
        extra['tree_json'] = args['tree_json']
    if args['clean']:
        extra['clean'] = True
    if args['hashes_only']:
        extra['hashes_only'] = True
    if args['no_hashes']:
        extra['no_hashes'] = True
    if args['update']:
        extra['update'] = True
    if args['contests_names']:
        extra['contests_names'] = True
    extra['start_from'] = args['start_from']



    if action == 'stat':
        preset = args['preset'] or die(tool_config.get_presets_info())
        return 'stat', preset, database_name, outfile, filters, extra
    else:
        if 'fill' not in config:
            die('Database config not found')
        base_dir = config['fill'].get('base_dir') or die('Base directory not specified')
        origin = config['fill'].get('origin') or die('Origin not specified')
        contests_info_dir = config['fill'].get('contests_info_dir')
        try:
            mysql_config = {
                'user': config['fill']['mysql_user'],
                'password': config['fill']['mysql_password'],
                'host': config['fill']['mysql_host'],
                'port': config['fill']['mysql_port'],
                'database': config['fill']['mysql_db_name']
            }
        except KeyError:
            die('Unable to parse MySQL config')
        return 'fill', database_name, base_dir, contests_info_dir, mysql_config, origin, extra


def main():
    args = get_arguments()
    if args[0] == 'fill':
        db_tool.fill_database(*args[1:] + (SCHEMA_VERSION,))
    elif args[0] == 'stat':
        connector = SQLiteConnector()
        connector.create_connection(args[2])
        update_db.start_update(connector, SCHEMA_VERSION)
        StatClass = tool_config.get_stat_by_preset(args[1])
        if StatClass is None:
            print('No such statistics')
            die(tool_config.get_presets_info())
        stat = StatClass(connector, args[4], args[5])
        stat.save_to_file(args[3])
        connector.close_connection()


if __name__ == "__main__":
    main()
