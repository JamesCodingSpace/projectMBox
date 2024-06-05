import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit, QVBoxLayout, QWidget, QListWidgetItem, QLabel, QAction, QToolBar, QMenu, QPushButton
from PyQt5.QtCore import Qt
import subprocess
import os

sys.path.append("mbox/settings")
from pid import pid_new_id, get_user

class EmailRecover(QMainWindow):
    def __init__(self):
        username = get_user()
        super().__init__()
        self.setWindowTitle(f"Gelöschte E-Mails von {username}")
        self.setGeometry(100, 100, 600, 400)

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

        self.sort_button = QPushButton("Sortieren", self)
        self.sort_menu = QMenu()

        sender_sort_action = QAction("Absender", self)
        sender_sort_action.triggered.connect(lambda: self.sort_emails("sender"))
        self.sort_menu.addAction(sender_sort_action)

        date_sort_action = QAction("Sendedatum", self)
        date_sort_action.triggered.connect(lambda: self.sort_emails("sent_date"))
        self.sort_menu.addAction(date_sort_action)

        subject_sort_action = QAction("Betreff", self)
        subject_sort_action.triggered.connect(lambda: self.sort_emails("subject"))
        self.sort_menu.addAction(subject_sort_action)

        self.sort_button.setMenu(self.sort_menu)
        self.toolbar.addWidget(self.sort_button)

        self.toolbar.addSeparator()

        settings_menu = QMenu()
        reload_mail = QAction("E-Mails Aktualisieren", self)
        reload_mail.triggered.connect(self.reload_emails)
        settings_menu.addAction(reload_mail)
    
        settings_action = QAction("Einstellungen", self)
        settings_action.setMenu(settings_menu)
        self.toolbar.addAction(settings_action)

        new_email_action = QAction("E-Mail Wiederherstellen", self)
        new_email_action.triggered.connect(self.recover_mail)
        self.toolbar.addAction(new_email_action)

        self.reply_action = QAction("Antworten", self)
        self.reply_action.setVisible(False)
        self.reply_action.triggered.connect(self.reply_email)
        self.toolbar.addAction(self.reply_action)

        self.forward_action = QAction("Weiterleiten", self)
        self.forward_action.setVisible(False)
        self.forward_action.triggered.connect(self.forward_email)
        self.toolbar.addAction(self.forward_action)

        self.delete_email_action = QAction("E-Mail Permanent Löschen", self)
        self.delete_email_action.triggered.connect(self.perm_delete_email)
        self.delete_email_action.setVisible(False)
        self.toolbar.addAction(self.delete_email_action)

    def load_emails(self, username): # lädt die gelöschten Emails des aktiven Users in ein sehr ähnlich aussehendes Fenster
        conn = sqlite3.connect('mbox/emails.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT eid, sender, subject, content, sent_date FROM deletedMails WHERE deletedFrom=? ORDER BY sent_date DESC", (username,))
        emails = cursor.fetchall()
        for email in emails:
            eid, sender, subject, _, _= email
            item = QListWidgetItem(f"{sender}\n{subject}")
            item.setData(Qt.UserRole, eid)
            self.email_list.addItem(item)
        conn.close()

    def recover_mail(self): # Fügt die Mail wieder in die Tabelle des Users ein
        selected_item = self.email_list.currentItem()
        if selected_item:
            eid = selected_item.data(Qt.UserRole)
            username = get_user()

            conn = sqlite3.connect('mbox/emails.db')
            cursor = conn.cursor()

            cursor.execute(f"SELECT eid, sender, subject, content, sent_date FROM deletedMails WHERE eid=?", (eid,))
            email = cursor.fetchone()

            if email:
                cursor.execute(f"INSERT INTO {username} (eid, sender, subject, content, sent_date) VALUES (?, ?, ?, ?, ?)",
                                (*email,))
                cursor.execute(f"DELETE FROM deletedMails WHERE eid = ?", (eid,))
                conn.commit()

                self.email_list.takeItem(self.email_list.currentRow())

            conn.close() 

    def get_email_data(self): # selbiges wie bei app_mail.py
        selected_item = self.email_list.currentItem()
        eid = selected_item.data(Qt.UserRole)
        username = get_user()
        conn = sqlite3.connect("mbox/emails.db")
        cursor = conn.cursor()
        with open("mbox/toolbar/email_data.tmp", "w") as file:
            cursor.execute(f"SELECT sender, subject, content, sent_date FROM deletedMails WHERE eid = {eid}")
            for row in cursor.fetchall():
                sender, subject, content, sent_date = row
                file.write(f"Sender: {sender}\n")
                file.write(f"Subject: {subject}\n")
                file.write(f"Content: {content}\n")
                file.write(f"Date: {sent_date}\n")
            conn.close()

    def reply_email(self): # öffnet neues Fenster
        self.get_email_data()
        subprocess.run(["python", "mbox/toolbar/answer_mail.py"])

    def forward_email(self): # öffnet neues Fenster
        self.get_email_data()
        subprocess.run(["python", "mbox/toolbar/forward_mail.py"])

    def reload_emails(self):
        username = get_user()
        self.email_list.clear()
        self.load_emails(username)
      
    def perm_delete_email(self):  # löscht Emails permanent
        selected_item = self.email_list.currentItem()
        if selected_item:
            eid = selected_item.data(Qt.UserRole)

            conn = sqlite3.connect('mbox/emails.db')
            cursor = conn.cursor()

            cursor.execute('''DELETE FROM deletedMails WHERE eid=?''', (eid,))
            conn.commit()

            self.email_list.takeItem(self.email_list.currentRow())
            conn.close()

    def on_email_selected(self):
        selected_item = self.email_list.currentItem()
        if selected_item:
            eid = selected_item.data(Qt.UserRole)
            username = get_user()
            conn = sqlite3.connect("mbox/emails.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT sender, subject, content, sent_date FROM deletedMails WHERE eid=?", (eid,))
            result = cursor.fetchone()
            conn.close()

            if result:
                sender, subject, content, sent_date = result
                email_info_text = f"Absender: {sender}\nBetreff: {subject}\nSendedatum: {sent_date}"
                self.email_info.setText(email_info_text)
                self.email_content.setPlainText(content)
                self.reply_action.setVisible(True)
                self.forward_action.setVisible(True)
                self.delete_email_action.setVisible(True)

    def sort_emails(self, column):
        self.email_list.clear()
        username = get_user()
        conn = sqlite3.connect('mbox/emails.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT eid, sender, subject, content, sent_date FROM {username} ORDER BY {column} DESC")
        emails = cursor.fetchall()
        conn.close()

        for email in emails:
            eid, sender, subject, _, _ = email
            item = QListWidgetItem(f"{sender}\n{subject}")
            item.setData(Qt.UserRole, eid)
            self.email_list.addItem(item)


def main():
    app = QApplication(sys.argv)
    recover = EmailRecover()
    recover.show()
    pid = os.getpid()
    pid_new_id("recover_mails.py", pid)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
