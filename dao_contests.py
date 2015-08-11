import model


class DAOContests:
    columns = 'id, contest_id, origin, name, scoring'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = model.Contest(row['contest_id'], row['origin'], row['name'], row['scoring'])
        return result

    def deep_load(self, row):
        return DAOContests.load(row)
