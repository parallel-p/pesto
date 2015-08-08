import xml.etree.ElementTree as ETree


def ejudge_get_contest_name(xml_filename):
    with open(xml_filename, encoding='utf-8') as f:
        data = f.read()
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        return None
    try:
        return xml_root.find("name").text
    except AttributeError:
        return None
