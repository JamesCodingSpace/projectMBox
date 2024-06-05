import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from premade_mails import insert_dummy_emails 
import random

class RegisterTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrierung")
        self.init_ui()
        self.create_database()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Benutzername:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.email_label = QLabel("E-Mail:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Passwort:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.password_repeat_label = QLabel("Passwort wiederholen:")
        self.password_repeat_input = QLineEdit()
        self.password_repeat_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_repeat_label)
        layout.addWidget(self.password_repeat_input)

        self.register_button = QPushButton("Registrieren")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def create_database(self): # Erstellt sofern noch nicht vorhanden die Logins Datenbank
        self.connection_logins = sqlite3.connect("mbox/login/logins.db")
        self.cursor_logins = self.connection_logins.cursor()

        self.cursor_logins.execute('''CREATE TABLE IF NOT EXISTS logins (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password TEXT NOT NULL,
                                userid INTEGER NOT NULL
                             )''')
        self.connection_logins.commit()

    def create_email_table(self, name): # Erstellt eigene Tabelle in Emails.db für den neuen User
        self.connection_emails = sqlite3.connect("mbox/emails.db")
        self.cursor_emails = self.connection_emails.cursor()

        table_name = name.replace(" ", "_") 
        self.cursor_emails.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                    id INTEGER PRIMARY KEY,
                                    eid FLOAT NOT NULL,
                                    sender TEXT NOT NULL,
                                    subject TEXT NOT NULL,
                                    content TEXT NOT NULL,
                                    sent_date TEXT NOT NULL
                                 )''')
        self.connection_emails.commit()

    def register(self): # Funktion Registrierung
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        password_repeat = self.password_repeat_input.text()

        if self.check_existing(email, name):
            QMessageBox.warning(self, "Registrierung fehlgeschlagen", "Die E-Mail oder der Benutzername existieren bereits.")
        elif password != password_repeat:
            QMessageBox.warning(self, "Registrierung fehlgeschlagen", "Die Passwörter stimmen nicht überein.")
        else:
            self.save_to_database(name, email, password)
            self.create_email_table(name)
            insert_dummy_emails(name)
            QMessageBox.information(self, "Registrierung erfolgreich", "Ihr Konto wurde erfolgreich erstellt.")
            sys.exit(app.exec_())

    def check_existing(self, email, name): # Überprüft ob User oder Email bereits vergeben ist
        self.cursor_logins.execute("SELECT * FROM logins WHERE email=? OR username=?", (email, name))
        user_info = self.cursor_logins.fetchone()
        return user_info is not None

    def save_to_database(self, name, email, password): # Speichert neuen User in der Datenbank
        name = name.replace(" ", "_")
        self.cursor_logins.execute("INSERT INTO logins (username, email, password, userid) VALUES (?, ?, ?, ?)", (name, email, password, random.randint(1, 1000000)))
        self.connection_logins.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterTerminal()
    window.show()
    sys.exit(app.exec_())
