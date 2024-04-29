import subprocess
import sys
import sqlite3
import signal

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

import os
sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search

class LoginTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Terminal")
        self.init_ui()
        self.create_database()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Benutzername/E-Mail:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Passwort:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Registrieren")
        self.register_button.clicked.connect(self.open_registration)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def create_database(self):
        self.connection = sqlite3.connect("mbox/login/logins.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logins (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password TEXT NOT NULL,
                                userid INTEGER NOT NULL
                             )''')
        self.connection.commit()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        self.cursor.execute("SELECT * FROM logins WHERE username=? OR email=?", (username, username))
        user_info = self.cursor.fetchone()

        if user_info:
            stored_password = user_info[3]
            if password == stored_password:
                self.save_loggedin_user(username)
                QMessageBox.information(self, "Login erfolgreich", f"Herzlich willkommen, {username}!")
                subprocess.run(["python", "mbox/app_main_test.py"])
                sys.exit(app.exec_())
            else:
                QMessageBox.warning(self, "Login fehlgeschlagen", "Ungültiges Passwort.")
        else:
            QMessageBox.warning(self, "Login fehlgeschlagen", "Benutzer nicht gefunden.")

    def open_registration(self):
        subprocess.run(["python", "mbox/login/signup.py"])

    def save_loggedin_user(self, username):
        # Verbindung zur SQLite-Datenbank herstellen
        connection = sqlite3.connect("mbox/settings/settings.db")
        cursor = connection.cursor()

        # Überprüfen, ob die Tabelle user existiert, andernfalls erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY,
                            username TEXT
                            )''')

        # Benutzernamen in die Tabelle einfügen oder aktualisieren
        cursor.execute("INSERT OR REPLACE INTO user (id, username) VALUES (1, ?)", (username,))
        connection.commit()
        connection.close()  

    def __del__(self):
        self.connection.close()

    def loggedout(self):
        connection = sqlite3.connect("mbox/settings/settings.db")
        cursor = connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO user (id, username) VALUES (1, ?)", ("Logged Out"))
        connection.commit()
        connection.close() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginTerminal()
    window.show()
    pid = os.getpid()
    pid_new_id("login.py", pid)
    sys.exit(app.exec_())
