import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import os
import subprocess
import signal

sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search, get_user

class PasswordConfirmation(QWidget):
    def __init__(self):
        super().__init__()
        username = get_user()
        self.setWindowTitle('Passwortbestätigung')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.label_username = QLabel(f'Benutzername: {username}')
        layout.addWidget(self.label_username)

        self.label_password = QLabel('Bitte geben sie erneut ihr Passwort ein:')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.button_confirm = QPushButton('Bestätigen')
        self.button_confirm.clicked.connect(self.confirm_password)
        layout.addWidget(self.button_confirm)

        self.setLayout(layout)

    def confirm_password(self):
        username = get_user()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Fehler', 'Bitte geben Sie ihr Passwort ein.')
            return

        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect('mbox/login/logins.db')
        cursor = conn.cursor()

        # Passwort aus der Datenbank abrufen
        cursor.execute("SELECT password FROM logins WHERE username=?", (username,))
        result = cursor.fetchone()

        if result is None:
            QMessageBox.warning(self, 'Fehler', 'Benutzername nicht gefunden.')
        elif password == result[0]:
            subprocess.run(["python","mbox/toolbar/change_account_info.py"])
            os.kill(pid_search("check_user_password.py"), signal.SIGTERM)
        else:
            QMessageBox.warning(self, 'Fehler', 'Falsches Passwort.')

        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordConfirmation()
    window.show()
    pid = os.getpid()
    pid_new_id("check_user_password.py", pid)
    sys.exit(app.exec_())
