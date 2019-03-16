class BooksModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='books'")
        row = cursor.fetchone()
        if row is None:
            self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             avtor VARCHAR(100),
                             name_book TEXT,
                             kol INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, avtor, name_book, kol):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO books
                          (avtor, name_book, kol)
                          VALUES (?,?,?)''', (avtor, name_book, str(kol) ))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None, sort='1'):
        if sort == '0':
            order = ' ORDER BY avtor DESC'
        else:
            order = ' ORDER BY avtor'
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM books WHERE user_id = ?" + order,
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM books" + order)
        rows = cursor.fetchall()
        return rows

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM books WHERE id = ?''', (str(user_id),))
        cursor.close()
        self.connection.commit()