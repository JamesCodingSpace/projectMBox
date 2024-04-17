import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class RegisterTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrierung")
        self.init_ui()

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

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if self.check_existing(email, name):
            QMessageBox.warning(self, "Registrierung fehlgeschlagen", "Die E-Mail oder der Benutzername existieren bereits.")
        else:
            self.save_to_file(name, email, password)
            QMessageBox.information(self, "Registrierung erfolgreich", "Ihr Konto wurde erfolgreich erstellt.")
            sys.exit(app.exec_())

    def check_existing(self, email, name):
        with open("signup/logins.txt", "r") as file:
            for line in file:
                if email in line or name in line:
                    return True
        return False

    def save_to_file(self, name, email, password):
        with open("signup/logins.txt", "a") as file:
            file.write(f"Benutzername: {name}, E-Mail: {email}, Passwort: {password}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterTerminal()
    window.show()
    sys.exit(app.exec_())
