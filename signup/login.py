import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import subprocess
import os

class LoginTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Terminal")
        self.init_ui()

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

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        with open("signup/logins.txt", "r") as file:
            for line in file:
                info = line.strip().split(", ")
                user_info = {x.split(": ")[0]: x.split(": ")[1] for x in info}
                if user_info["Benutzername"] == username or user_info["E-Mail"] == username:
                    if user_info["Passwort"] == password:
                        self.save_loggedin_user(username)
                        QMessageBox.information(self, "Login erfolgreich", f"Herzlich willkommen, {username}!")
                        return
                    else:
                        QMessageBox.warning(self, "Login fehlgeschlagen", "Ungültiges Passwort.")
                        return
        QMessageBox.warning(self, "Login fehlgeschlagen", "Benutzer nicht gefunden.")

    def open_registration(self):
        subprocess.run(["python", "signup/signup.py"])

    def save_loggedin_user(self, username):
        with open("mbox/settings/settings.txt", "w") as file:
            file.write(f"Benutzername: {username}\n")    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginTerminal()
    window.show()
    sys.exit(app.exec_())
