import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
import os
import subprocess
import signal
sys.path.append("mbox/settings")
from pid import pid_search

def logout():
    confirm = QMessageBox.question(None, "Abmelden", "Möchten Sie sich wirklich abmelden?",
    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if confirm == QMessageBox.Yes:
        # Datei überschreiben
        with open("mbox/settings/settings.txt", "w") as file:
            file.write("Logged Out")
        os.kill(pid_search("app_main.py"), signal.SIGTERM)
        subprocess.run(["python", "mbox/login/login.py"])
    if confirm == QMessageBox.No: 
        os.kill(pid_search("app_main.py"))
        subprocess.run(["python", "mbox/app_main.py"])

# GUI initialisieren
app = QApplication(sys.argv)

# Dialogfenster anzeigen
logout()

# GUI beenden
sys.exit(app.exec_())
