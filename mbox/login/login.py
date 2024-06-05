import subprocess
import sys
import sqlite3
import signal
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

import os
sys.path.append("mbox/settings")
from pid import pid_new_id, pid_search

class LoginTerminal(QWidget): # Klasse die das Login Fenster erstellt
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Terminal") # FensterName bestimmen
        self.init_ui()
        self.close_change_account_info()
        self.create_database()

    def init_ui(self): # UserInterface aufbauen
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

    def close_change_account_info(self):  # Sofern User Bereits angemeldet war und seine Acc Info geändert hat wird er ausgeloggt, hier wird das Fenster zum verändern der Informationen geschlossen
        if os.path.exists("mbox/toolbar/close_window.tmp"):
            try:
                with open("mbox/toolbar/close_window.tmp", 'r') as file:
                    for line in file:
                        if 'close' in line:
                                os.kill(pid_search("change_account_info.py"), signal.SIGTERM)
                                os.remove("mbox/toolbar/close_window.tmp")
            finally:
                None               

    def create_database(self): # erstellt sofern noch nicht vorhanden die Datenbank in der die Login Daten gespeichert werden
        self.connection = sqlite3.connect("mbox/login/logins.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logins (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password TEXT NOT NULL,
                                userid INTEGER NOT NULL
                             )''')
        self.connection.commit()

    def login(self): # Login Prozress
        username = self.username_input.text()
        password = self.password_input.text()

        self.cursor.execute("SELECT * FROM logins WHERE username=? OR email=?", (username, username))
        user_info = self.cursor.fetchone()

        if user_info: # Überprüft nach Eingabe der Daten ob es einen Benutzer mit den Daten gibt
            stored_password = user_info[3]
            if password == stored_password:
                self.save_loggedin_user(username)
                QMessageBox.information(self, "Login erfolgreich", f"Herzlich willkommen, {username}!")
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open ("mbox/login/login.log", "a") as file: # Speichert Anmeldeverlauf in "Login.log"
                    file.write(f"{time}: {username}\n")    
                subprocess.run(["python", "mbox/app_main.py"])
                sys.exit(app.exec_())
            else:
                QMessageBox.warning(self, "Login fehlgeschlagen", "Ungültiges Passwort.")
        else:
            QMessageBox.warning(self, "Login fehlgeschlagen", "Benutzer nicht gefunden.")

    def open_registration(self): # öffnet Fenster zum Registrieren
        subprocess.run(["python", "mbox/login/signup.py"])

    def save_loggedin_user(self, username): # Speichert welcher User sich angemeldet hat
        # Verbindung zur SQLite-Datenbank herstellen
        connection = sqlite3.connect("mbox/settings/settings.db")
        cursor = connection.cursor()

        # Überprüfen, ob die Tabelle user existiert, andernfalls erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY,
                            username TEXT
                            )''')

        # Benutzernamen in die Tabelle einfügen oder aktualisieren
        cursor.execute("INSERT OR REPLACE INTO user (id, username) VALUES (1, ?)", (username,))
        connection.commit()
        connection.close()  

    def __del__(self): # schließt Verbindung zur Datenbank
        self.connection.close()

    def loggedout(self): # speichert, dass User nun ausgeloggt ist
        connection = sqlite3.connect("mbox/settings/settings.db")
        cursor = connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO user (id, username) VALUES (1, ?)", ("Logged Out"))
        connection.commit()
        connection.close() 


if __name__ == "__main__": # Initialisiert das Login Fenster
    app = QApplication(sys.argv)
    window = LoginTerminal()
    window.show()
    pid = os.getpid()
    pid_new_id("login.py", pid) # Speichert PID (Program ID) zum schließen später
    sys.exit(app.exec_())
