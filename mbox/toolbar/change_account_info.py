import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import os
import signal
import subprocess

sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search, get_user

class AccountSettings(QWidget):
    def confirm_changes(self):
        new_name = self.input_name.text().strip()
        new_email = self.input_email.text().strip()
        new_password = self.input_new_password.text().strip()
        confirm_password = self.input_confirm_password.text().strip()

        if not new_name and not new_email and not new_password and not confirm_password:
            QMessageBox.warning(self, 'Fehler', 'Bitte geben Sie mindestens eine Änderung ein.')
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, 'Fehler', 'Die neuen Passwörter stimmen nicht überein.')
            return

        conn = sqlite3.connect('mbox/login/logins.db')
        cursor = conn.cursor()

        username = get_user()
        cursor.execute(f"SELECT userid FROM logins WHERE username=?", (username,)) #Lösungsansätze: 1. statt * wirklich nur nötiges rausziehen und dann neu einfügen
        result = cursor.fetchone()                                            #2. User Speziefische ID einfügen, welche sich nicht verändert und damit den Change unten machen
        if result is not None:
            result = result[0]

        if new_name:
            cursor.execute("UPDATE logins SET username=? WHERE userid=?", (new_name, result,))
            rename_table("mbox/emails.db", username, new_name)

        if new_email:
            cursor.execute("UPDATE logins SET email=? WHERE userid=?", (new_email, result,))

        if new_password:
            cursor.execute(f"UPDATE logins SET password=? WHERE userid=?", (new_password, result,))

        with open("mbox/settings/settings.txt", "w") as file:
            file.write("Logged Out")
        os.kill(pid_search("app_main.py"), signal.SIGTERM)
        QMessageBox.information(self, 'Erfolg', 'Änderungen wurden gespeichert.')
        subprocess.run(["python", "mbox/login/login.py"])
        conn.commit()
        conn.close()
        os.kill(pid_search("change_account_info.py"), signal.SIGTERM)

    def delete_account(self):
        QMessageBox.warning(self, 'Achtung', 'Sind Sie sicher, dass Sie Ihren Account löschen möchten? Diese Aktion kann nicht rückgängig gemacht werden.')

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Account Informationen ändern')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label_name = QLabel('Neuer Name:')
        self.input_name = QLineEdit()
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)

        self.label_email = QLabel('Neue Email:')
        self.input_email = QLineEdit()
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)

        self.label_new_password = QLabel('Neues Passwort:')
        self.input_new_password = QLineEdit()
        self.input_new_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_new_password)
        layout.addWidget(self.input_new_password)

        self.label_confirm_password = QLabel('Passwort Bestätigen:')
        self.input_confirm_password = QLineEdit()
        self.input_confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_confirm_password)
        layout.addWidget(self.input_confirm_password)

        self.button_confirm_changes = QPushButton('Änderungen bestätigen')
        self.button_confirm_changes.clicked.connect(self.confirm_changes)
        layout.addWidget(self.button_confirm_changes)

        self.button_delete_account = QPushButton('Account löschen')
        self.button_delete_account.clicked.connect(self.delete_account)
        layout.addWidget(self.button_delete_account)

        self.setLayout(layout)

def rename_table(db_file, old_table_name, new_table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE TABLE {new_table_name} AS SELECT * FROM {old_table_name}")
        cursor.execute(f"DROP TABLE {old_table_name}")
        conn.commit()
    except Exception as e:
        print("Fehler beim Umbenennen der Tabelle:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AccountSettings()
    window.show()
    pid = os.getpid()
    pid_new_id("change_account_info.py", pid)
    os.kill(pid_search("check_user_password.py"), signal.SIGTERM)
    sys.exit(app.exec_())
