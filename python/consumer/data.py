from os.path import isfile
import sqlite3
import os

class Data:
    filename = 'users.db'

    def __init__(self):
        if not os.path.isfile(self.filename):
            self.create_table()
            self.insert_email('abenitof@hotmail.com')


    def connect(self):
        self.db = sqlite3.connect('users.db')

    def insert_email(self, new_email):
        self.connect()
        self.db.execute(f"INSERT INTO user VALUES('{new_email}')")
        self.db.commit()
        self.db.close()
        
    def create_table(self):
        self.connect()
        self.db.execute("CREATE TABLE user(email)")
        self.db.close()

    def get_emails(self):
        self.connect()
        result = self.db.execute("SELECT email FROM user")
        emails = [r[0] for r in result]
        self.db.close()
        return emails
