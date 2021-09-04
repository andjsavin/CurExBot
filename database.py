import sqlite3

class dataBase:
    def __init__(self, dbname="exRates.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (base text, comp text, rate text, saved text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, base, comp, rate, saved):
        stmt = "INSERT INTO items (base, comp, rate, saved) VALUES (?, ?, ?, ?)"
        args = (base, comp, rate, saved,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, base):
        stmt = "DELETE FROM items WHERE base = (?)"
        args = (base,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item_by_comp(self, base, comp):
        stmt = "DELETE FROM items WHERE (base, comp) = (?, ?)"
        args = (base, comp, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, base):
        stmt = "SELECT * FROM items WHERE base = (?)"
        args = (base, )
        return [[x[0], x[1], x[2], x[3]] for x in self.conn.execute(stmt, args)]

    def get_exchange(self, base, comp):
        stmt = "SELECT * FROM items WHERE (base, comp) = (?, ?)"
        args = (base, comp, )
        return [[x[0], x[1], x[2], x[3]] for x in self.conn.execute(stmt, args)]