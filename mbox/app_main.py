import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit, QVBoxLayout, QWidget, QListWidgetItem, QLabel, QAction, QToolBar, QMenu
import subprocess
import os
import signal
from PyQt5.QtCore import Qt

sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search, get_user

class EmailClient(QMainWindow):
    def __init__(self):
        username = get_user()
        super().__init__()
        self.setWindowTitle(f"E-Mail Postfach von {username}")
        self.setGeometry(100, 100, 800, 600)

        self.create_toolbar()

        splitter = QSplitter(self)
        self.setCentralWidget(splitter)

        left_layout = QVBoxLayout()

        self.email_info = QLabel()
        left_layout.addWidget(self.email_info)

        self.email_content = QTextEdit()
        self.email_content.setReadOnly(True)
        splitter.addWidget(self.email_content)

        self.email_list = QListWidget()
        self.email_list.itemSelectionChanged.connect(self.on_email_selected)
        left_layout.addWidget(self.email_list)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        sizes = [self.width() // 5 * 4, self.width() // 5]
        splitter.setSizes(sizes)

        self.load_emails(username)

    def create_toolbar(self):
        self.toolbar = self.addToolBar("Toolbar")

        settings_menu = QMenu()
        logout_action = QAction("Abmelden", self)
        logout_action.triggered.connect(self.logout)
        settings_menu.addAction(logout_action)
        credits_action = QAction("Credits", self)
        credits_action.triggered.connect(self.show_credits)
        settings_menu.addAction(credits_action)
        shutdown_action = QAction("Schließen", self)
        shutdown_action.triggered.connect(self.shutdown)
        settings_menu.addAction(shutdown_action)

        settings_action = QAction("Einstellungen", self)
        settings_action.setMenu(settings_menu)
        self.toolbar.addAction(settings_action)

        new_email_action = QAction("E-Mail Schreiben", self)
        new_email_action.triggered.connect(self.write_email)
        self.toolbar.addAction(new_email_action)

        self.reply_action = QAction("Antworten", self)
        self.reply_action.setVisible(False)
        self.reply_action.triggered.connect(self.reply_email)
        self.toolbar.addAction(self.reply_action)

        self.forward_action = QAction("Weiterleiten", self)
        self.forward_action.setVisible(False)
        self.forward_action.triggered.connect(self.forward_email)
        self.toolbar.addAction(self.forward_action)

        self.delete_email_action = QAction("E-Mail Löschen", self)
        self.delete_email_action.triggered.connect(self.delete_email)
        self.delete_email_action.setVisible(False)
        self.toolbar.addAction(self.delete_email_action)

    def load_emails(self, username):
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect('mbox/emails.db')
        cursor = conn.cursor()

        # Abfrage ausführen, um E-Mails des Benutzers abzurufen
        cursor.execute(f"SELECT eid, sender, subject, content, sent_date FROM {username}")
        emails = cursor.fetchall()

        # E-Mails zur Liste hinzufügen
        for email in emails:
            eid, sender, subject, _, _ = email
            item = QListWidgetItem(f"{sender}\n{subject}")
            item.setData(Qt.UserRole, eid)  # ID des Eintrags als Benutzerdaten setzen
            self.email_list.addItem(item)

        conn.close()

    def write_email(self):
        subprocess.run(["python", "mbox/toolbar/send_mail.py"])

    def reply_email(self):
        print("Antwort auf E-Mail verfassen")

    def forward_email(self):
        print("E-Mail weiterleiten")

    def delete_email(self):
        print("E-Mail löschen")

    def logout(self):
        subprocess.run(["python", "mbox/settings/logout.py"])

    def show_credits(self):
        subprocess.run(["python", "mbox/settings/credits.py"])

    def shutdown(self):
        with open("mbox/settings/settings.txt", "w") as file:
            file.write("Logged Out")
        os.kill(pid_search("app_main.py"), signal.SIGTERM)

    def on_email_selected(self):
        selected_item = self.email_list.currentItem()
        username = get_user()
        if selected_item:
            eid = selected_item.data(Qt.UserRole)  # Die ID des ausgewählten Elements abrufen
            conn = sqlite3.connect("mbox/emails.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT sender, subject, content, sent_date FROM {username} WHERE eid = {eid}")
            result = cursor.fetchone()
            conn.close()

            if result:
                sender, subject, content, sent_date = result
                email_info_text = f"Absender: {sender}\nBetreff: {subject}\nSendedatum: {sent_date}"
                self.email_info.setText(email_info_text)
                self.email_content.setPlainText(content)
                self.toolbar.removeAction(self.delete_email_action)
                self.toolbar.addAction(self.delete_email_action)
                self.reply_action.setVisible(True)
                self.forward_action.setVisible(True)
                self.delete_email_action.setVisible(True)



def main():
    app = QApplication(sys.argv)
    client = EmailClient()
    client.show()
    pid = os.getpid()
    pid_new_id("app_main.py", pid)
    os.kill(pid_search("login.py"), signal.SIGTERM)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
