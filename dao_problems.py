from model import Problem


class DAOProblems:
    @staticmethod
    def load(row):
        result = Problem(row[2], row[3], [])
        return result