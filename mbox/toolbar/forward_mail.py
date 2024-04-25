import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from datetime import datetime
import os
import signal
import random

sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search, get_user


class EmailReply(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antworten auf E-Mail")
        username = get_user()
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

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

        self.reply_button = QPushButton("Antworten")
        self.reply_button.clicked.connect(self.send_forward)
        input_layout.addWidget(self.reply_button)

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
        connection = sqlite3.connect('mbox/login/logins.db')
        cursor = connection.cursor()

        sql_query = "SELECT username, email FROM logins"
        cursor.execute(sql_query)

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

    def send_forward(self):
        sender = get_user()
        recipient = self.recipient_input.text()
        subject = self.subject_input.text()
        content = self.content_input.toPlainText()

        if not recipient or not subject or not content:
            print("Bitte füllen Sie alle Felder aus.")
            return

        conn = sqlite3.connect("mbox/emails.db")
        cursor = conn.cursor()

        sent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rndm_eid = random.randint(1,1000000000000)

        cursor.execute(f"INSERT INTO {recipient} (eid, sender, subject, content, sent_date) VALUES (?, ?, ?, ?, ?)",
                       (rndm_eid, sender, subject, content, sent_date))
        conn.commit()
        conn.close()

        os.kill(pid_search("forward_mail.py"), signal.SIGTERM)


def main():
    app = QApplication(sys.argv)
    with open("mbox/toolbar/email_data.tmp", "r") as file:
        data = file.read().splitlines()   
    sender = None
    subject = None
    content = None
    date = None
    for line in data:
        if line.startswith("Sender:"):
            sender = line.split(": ")[1]
        elif line.startswith("Subject:"):
            subject = line.split(": ")[1]
        elif line.startswith("Content:"):
            content = line.split(": ")[1]
        elif line.startswith("Date:"):
            date = line.split(": ")[1]
    os.remove("mbox/toolbar/email_data.tmp")

    if sender and subject and content:
        reply_window = EmailReply()
        reply_window.subject_input.setText("Fwd: " + subject)
        reply_window.content_input.setPlainText(f"\n\nAm {date}\nschrieb mir {sender}:\n\n" + content)
        reply_window.show()
        pid = os.getpid()
        pid_new_id("forward_mail.py", pid)
        sys.exit(app.exec_())
    


if __name__ == "__main__":
    main()
