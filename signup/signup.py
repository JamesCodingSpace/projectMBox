import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

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

        self.register_button = QPushButton("Registrieren")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def create_database(self):
        # Connect to the logins database
        self.connection_logins = sqlite3.connect("signup/logins.db")
        self.cursor_logins = self.connection_logins.cursor()

        # Create logins table if not exists
        self.cursor_logins.execute('''CREATE TABLE IF NOT EXISTS logins (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password TEXT NOT NULL
                             )''')
        self.connection_logins.commit()

    def create_email_table(self, name):
        # Connect to the emails database
        self.connection_emails = sqlite3.connect("mbox/emails.db")
        self.cursor_emails = self.connection_emails.cursor()

        # Create table for the user's emails
        table_name = name.replace(" ", "_")  # Replace spaces in name with underscores for table name
        self.cursor_emails.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                    id INTEGER PRIMARY KEY,
                                    eid FLOAT NOT NULL,
                                    sender TEXT NOT NULL,
                                    subject TEXT NOT NULL,
                                    content TEXT NOT NULL,
                                    sent_date TEXT NOT NULL
                                 )''')
        self.connection_emails.commit()

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if self.check_existing(email, name):
            QMessageBox.warning(self, "Registrierung fehlgeschlagen", "Die E-Mail oder der Benutzername existieren bereits.")
        else:
            self.save_to_database(name, email, password)
            self.create_email_table(name)  # Create email table for the user
            QMessageBox.information(self, "Registrierung erfolgreich", "Ihr Konto wurde erfolgreich erstellt.")
            sys.exit(app.exec_())

    def check_existing(self, email, name):
        self.cursor_logins.execute("SELECT * FROM logins WHERE email=? OR username=?", (email, name))
        user_info = self.cursor_logins.fetchone()
        return user_info is not None

    def save_to_database(self, name, email, password):
        name = name.replace(" ", "_")
        self.cursor_logins.execute("INSERT INTO logins (username, email, password) VALUES (?, ?, ?)", (name, email, password))
        self.connection_logins.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterTerminal()
    window.show()
    sys.exit(app.exec_())
