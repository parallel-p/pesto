import xml.etree.ElementTree as ETree
import  logging


def ejudge_get_contest_name(xml_filename):
    try:
        with open(xml_filename, encoding='utf-8') as f:
            data = f.read()
    except UnicodeError:
        logging.warning('Unable to parse {}'.format(xml_filename))
        return None
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        logging.warning('Unable to parse {}'.format(xml_filename))
        return None
    try:
        return xml_root.find("name").text
    except AttributeError:
        logging.warning('Unable to parse {}'.format(xml_filename))
        return None
