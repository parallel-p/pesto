from dao_submits import DAOSubmits


def shard_by_scoring(connection, factory):
    visitor_acm = factory.create('ACM')
    visitor_kirov = factory.create('kirov')
    cursor = connection.get_cursor()
    cursor.execute('SELECT {} FROM Submits'.format(DAOSubmits.columns))
    dao = DAOSubmits(connection)
    for row in range(cursor.rowcount):
        submit = dao.deep_load(row)
        if submit.scoring == 'ACM':
            visitor_acm.visit(submit)
        else:
            visitor_kirov.visit(submit)
