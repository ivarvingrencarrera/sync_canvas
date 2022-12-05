import pyodbc

class Database():

    def __init__(self, connection)  -> None:
        self.connection = connection

    def set_connection(self, connection):
        connection.setencoding(encoding='utf-8')
        return connection

    def query(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def fetch(self, sql) -> list[dict]:
        rows: list[dict] = []
        cursor = self.query(sql)
        columns: list = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            rows.append(dict(zip(columns, row)))
        cursor.close()
        return rows

    def fetchone(self, sql) -> dict:
        cursor = self.query(sql)
        columns: list = [column[0] for column in cursor.description]
        row: dict = dict(zip(columns, cursor.fetchone()))
        cursor.close()
        return row

    def update(self, sql) -> None:
        status = True
        while status:
            try:
                cursor = self.query(sql)
                rowcount = cursor.rowcount
                self.connection.commit()
                status = False
            except pyodbc.Error as error:
                status = True if error.args[0] == 'HY007' else False
        cursor.close()   

    def __del__(self) -> None:
        if self.connection != None:
            self.connection.close()