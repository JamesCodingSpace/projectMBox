import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
import os
import subprocess

def logout():
    confirm = QMessageBox.question(None, "Abmelden", "Möchten Sie sich wirklich abmelden?",
    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if confirm == QMessageBox.Yes:
        # Datei überschreiben
        with open("mbox/settings/settings.txt", "w") as file:
            file.write("Logged Out")

        # Task schließen (für Windows)
        os.system("taskkill /f /im python.exe")
        subprocess.run(["python", "mbox/app_main_test.py"])

# GUI initialisieren
app = QApplication(sys.argv)

# Dialogfenster anzeigen
logout()

# GUI beenden
sys.exit(app.exec_())
