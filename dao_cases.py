class DAOCases():
    columns = "io_hash"

    def __init__(self, connector):
        self.connector = connector
    
    @staticmethod
    def load(row):
        result_hash = row['io_hash']
        return result_hash

    def deep_load(self, row):
        return self.load(row)
