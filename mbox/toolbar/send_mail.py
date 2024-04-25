import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from datetime import datetime
import random
import os
import signal

sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search, get_user


class EmailComposer(QMainWindow):
    def __init__(self):
        username = get_user()
        super().__init__()
        self.setWindowTitle("Neue E-Mail verfassen")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

        # Layout für Eingabefelder
        input_layout = QVBoxLayout()

        self.sender_label = QLabel(f"Absender: {username}")
        input_layout.addWidget(self.sender_label)

        self.recipient_label = QLabel("Empfänger:")
        self.recipient_input = QLineEdit()
        input_layout.addWidget(self.recipient_label)
        input_layout.addWidget(self.recipient_input)

        self.subject_label = QLabel("Betreff:")
        self.subject_input = QLineEdit()
        input_layout.addWidget(self.subject_label)
        input_layout.addWidget(self.subject_input)

        self.content_label = QLabel("Inhalt:")
        self.content_input = QTextEdit()
        input_layout.addWidget(self.content_label)
        input_layout.addWidget(self.content_input)

        self.send_button = QPushButton("Senden")
        self.send_button.clicked.connect(self.send_email)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        # Layout für Benutzerliste
        user_list_layout = QVBoxLayout()

        self.user_list_label = QLabel("Vorhandene Benutzer:")
        user_list_layout.addWidget(self.user_list_label)

        self.user_list_widget = QListWidget()
        self.populate_user_list()
        self.user_list_widget.clicked.connect(self.fill_recipient_field)
        user_list_layout.addWidget(self.user_list_widget)

        main_layout.addLayout(user_list_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def populate_user_list(self):
        # Verbindung zur SQLite-Datenbank herstellen
        connection = sqlite3.connect('mbox/login/logins.db')
        cursor = connection.cursor()

        # SQL-Abfrage zum Abrufen aller Benutzernamen und E-Mail-Adressen
        sql_query = "SELECT username, email FROM logins"
        cursor.execute(sql_query)

        # Alle Benutzer und deren E-Mails der Liste hinzufügen
        for row in cursor.fetchall():
            username, email = row
            item = QListWidgetItem(f"{username} ({email})")
            self.user_list_widget.addItem(item)

        connection.close()

    def fill_recipient_field(self):
        selected_item = self.user_list_widget.currentItem()
        if selected_item:
            username_email = selected_item.text()
            username = username_email.split(' ')[0]
            self.recipient_input.setText(username)

    def search_in_db(self, recipient):
        # Verbindung zur SQLite-Datenbank herstellen
        connection = sqlite3.connect('mbox/login/logins.db')
        cursor = connection.cursor()

        # SQL-Abfrage zum Suchen der Eingabe in den Spalten 1 und 2
        sql_query = "SELECT username FROM logins WHERE username = ? OR email = ?"
        cursor.execute(sql_query, (recipient, recipient))

        # Den Inhalt der ersten Spalte ausgeben, wenn ein Treffer gefunden wurde
        result = cursor.fetchone()
        if result:
            connection.close()
            return result[0]
        else:
            connection.close()
            return None

    def send_email(self):
        sender = get_user()
        recipient_input = self.recipient_input.text()
        recipient = self.search_in_db(recipient_input)
        subject = self.subject_input.text()
        content = self.content_input.toPlainText()

        if not recipient or not subject or not content:
            print("Bitte füllen Sie alle Felder aus.")
            return

        conn = sqlite3.connect('mbox/emails.db')
        cursor = conn.cursor()

        sent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rndm_eid = random.randint(1,1000000000000)

        # Einfügen der E-Mail in die Datenbank
        cursor.execute(f"INSERT INTO {recipient} (eid, sender, subject, content, sent_date) VALUES (?, ?, ?, ?, ?)",
                       (rndm_eid, sender, subject, content, sent_date))
        conn.commit()
        conn.close()

        os.kill(pid_search("send_mail.py"), signal.SIGTERM)


def main():
    app = QApplication(sys.argv)
    composer = EmailComposer()
    composer.show()
    pid = os.getpid()
    pid_new_id("send_mail.py", pid)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
