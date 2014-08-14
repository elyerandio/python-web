import sqlite3

class QuoteStorage(object):
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()


    def close(self):
        self.cursor.close()
        self.connection.close()


    def createDb(self):
        query = """CREATE TABLE quotes
                    (id INTEGER PRIMARY KEY, quote TEXT, author TEXT, category TEXT)"""
        self.cursor.execute(query)
        self.connection.commit()


    def addQuote(self, quote, author, category):
        self.cursor.execute("""INSERT INTO quotes
                            VALUES(?, ?, ?, ?)""", (None, quote, author, category))
        self.connection.commit()

    def getQuote(self, index = None):
        if index:
            self.cursor.execute("""SELECT * FROM quotes WHERE id=?""", (index,))
        else:
            self.cursor.execute("""SELECT * FROM quotes
                                ORDER by Random()
                                LIMIT 1""")
        res = self.cursor.fetchone()
        return res


if __name__ == '__main__':
    qs = QuoteStorage('quotes.db')
    """
    qs.createDb()
    qs.addQuote('akjdkjklsdf', 'qqqq', 'wwwww')
    qs.addQuote('jfka;jfkjaklfj', 'qqqq2', 'wwwww2')
    qs.addQuote('akjdkjklsdf', 'qqqq3', 'wwwww3')
    """
    print qs.getQuote(1)
    print qs.getQuote()
    qs.close()
