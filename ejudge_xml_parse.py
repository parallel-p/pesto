import xml.etree.ElementTree as ETree


class EjudgeXmlParseResult:
    def __init__(self, submit_id, submit_outcome, scoring, run_outcomes):
        self.submit_id = submit_id
        self.submit_outcome = submit_outcome
        self.scoring = scoring
        self.run_outcomes = run_outcomes


def ejudge_xml_parse(file):
    try:
        lines = file.readlines()  # invalid .gz
        if not lines:
            return None
        if type(lines[0]) == bytes:
            for i in range(len(lines)):
                lines[i] = lines[i].decode()
    except UnicodeError:
        return None
    # Removing first two lines, because they are not XML
    data = ''.join(lines[2:])
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        return None
    run_outcomes = []
    submit_id, submit_outcome, scoring = None, None, None
    for child in xml_root.iter():
        if child.tag == 'testing-report':
            submit_id = child.attrib['run-id']
            submit_outcome = child.attrib['status']
            scoring = child.attrib['scoring']
        elif child.tag == 'test':
            run_outcomes.append(
                (child.attrib.get('real-time', child.attrib['time']), child.attrib['time'], child.attrib['status']))
    if submit_id is None or submit_outcome is None or scoring is None:
        return None
    return EjudgeXmlParseResult(submit_id, submit_outcome, scoring, run_outcomes)
