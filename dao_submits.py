from model import Submit


class DAOSubmits:
    @staticmethod
    def load(cursor):
        response = cursor.fetchone()
        if response is None:
            return None
        submit = Submit(response[2], None, None, response[1], None, response[3], None, response[5])
