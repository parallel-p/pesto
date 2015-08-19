class DAOCases:
    columns = "io_hash"

    def __init__(self, connector):
        self.connector = connector
    
    @staticmethod
    def load(row):
        result_hash = row['io_hash']
        return result_hash

    def deep_load(self, row):
        return self.load(row)

    def define(self, problem_ref, case_id):
        ref = self.lookup(problem_ref, case_id)
        if ref is None:
            ref = self.create(problem_ref, case_id)
        return ref

    def lookup(self, problem_ref, case_id):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Cases WHERE problem_ref = ? AND case_id = ?', [problem_ref, case_id])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, problem_ref, case_id):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Cases (id, problem_ref, case_id) VALUES (NULL, ?, ?)', [problem_ref, case_id])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Cases WHERE id = ?'.format(self.columns), ref)
        old = self.load(cursor.fetchone())
        new_def = {'io_hash': old}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Cases SET io_hash = :io_hash WHERE id = :id', new_def)
