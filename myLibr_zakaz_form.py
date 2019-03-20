from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

class ZakazModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='zakaz'")
        row = cursor.fetchone()
        if row is None:
            self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS zakaz
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             book_id INTEGER,
                             user_id INTEGER,
                             pub_date INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, book_id, user_id):
        cursor = self.connection.cursor()
        pub_date = round(datetime.timestamp(datetime.now()))
        cursor.execute('''INSERT INTO zakaz
                          (book_id, user_id, pub_date)
                          VALUES (?,?,?)''', (str(book_id), str(user_id), pub_date))
        cursor.close()
        self.connection.commit()

    def get(self, zakaz_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM zakaz WHERE id = ?", (str(zakaz_id),))
        row = cursor.fetchone()
        return row

    def get_all(self,  sort='0'):
        if sort == '0':
            order = ' ORDER BY pub_date DESC'
        else:
            order = ' ORDER BY title'
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM zakaz" + order)
        rows = cursor.fetchall()
        return rows

    def delete(self, zakaz_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM zakaz WHERE id = ?''', (str(zakaz_id),))
        cursor.close()
        self.connection.commit()

    def del_all(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM zakaz")
        cursor.close()
        self.connection.commit()