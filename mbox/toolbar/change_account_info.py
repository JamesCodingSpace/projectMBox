import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import os
import signal
import subprocess

sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search, get_user

class AccountSettings(QWidget):
    def close_window(self):
        with open("mbox/toolbar/close_window.tmp", "w") as file:
            file.write("close")

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
        cursor.execute(f"SELECT userid FROM logins WHERE username=?", (username,)) # Fehler: Bei User @Test wurde Mail, Pw und Name nicht verändert -> Bei user Jamie jedoch schon => hängt fest im code?
        result = cursor.fetchone()                                            
        if result is not None:
            result = result[0]

        if new_name:
            print(new_name) # überprüfung ob code bis heirhin ausgefühlt wird => später noch entfernen
            cursor.execute(f"UPDATE logins SET username=? WHERE userid=?", (new_name, result,))
            rename_table("mbox/emails.db", username, new_name)
            print("finish1") # überprüfung ob code bis heirhin ausgefühlt wird => später noch entfernen

        if new_email:
            print(new_email) # überprüfung ob code bis heirhin ausgefühlt wird => später noch entfernen
            cursor.execute(f"UPDATE logins SET email=? WHERE userid=?", (new_email, result,))
            print("finish2") # überprüfung ob code bis heirhin ausgefühlt wird => später noch entfernen

        if new_password:
            print(new_password) # überprüfung ob code bis heirhin ausgefühlt wird => später noch entfernen
            cursor.execute(f"UPDATE logins SET password=? WHERE userid=?", (new_password, result,))
            print("finish3") # überprüfung ob code bis heirhin ausgefühlt wird => später noch entfernen

        conn.commit()
        conn.close()

        os.kill(pid_search("app_main.py"), signal.SIGTERM)
        self.close_window()
        subprocess.run(["python", "mbox/login/login.py"])
        sys.exit(app.exec_())

    def delete_account(self):
        username = get_user()
        conn = sqlite3.connect('mbox/login/logins.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT userid FROM logins WHERE username=?", (username,))
        result = cursor.fetchone()
        result = result[0]

        reply = QMessageBox.question(self, 'Achtung', 
            'Sind Sie sicher, dass Sie Ihren Account löschen möchten? Diese Aktion kann nicht rückgängig gemacht werden.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            cursor.execute('''DELETE FROM logins WHERE userid=?''', (result,))
            conn.commit()
            conn.close()
            conn = sqlite3.connect('mbox/emails.db')
            cursor = conn.cursor()
            cursor.execute(f'''DROP TABLE IF EXISTS {username}''')
            conn.commit()
            conn.close()
            os.kill(pid_search("app_main.py"), signal.SIGTERM)
            self.close_window()
            subprocess.run(["python", "mbox/login/login.py"])
            sys.exit(app.exec_())
        else:
            None

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
