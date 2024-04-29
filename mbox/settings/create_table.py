import sqlite3


connection = sqlite3.connect("mbox/settings/settings.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL
                             )''')

connection.close()