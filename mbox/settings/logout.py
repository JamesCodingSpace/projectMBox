import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
import os
import subprocess
import signal
import sqlite3
sys.path.append("mbox/settings")
from pid import pid_search

def logout():
    confirm = QMessageBox.question(None, "Abmelden", "Möchten Sie sich wirklich abmelden?",
    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if confirm == QMessageBox.Yes:
        connection = sqlite3.connect("mbox/settings/settings.db")
        cursor = connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO user (id, username) VALUES (1, ?)", (" "))
        connection.commit()
        connection.close() 
        os.kill(pid_search("app_main.py"), signal.SIGTERM)
        subprocess.run(["python", "mbox/login/login.py"])
    if confirm == QMessageBox.No: 
        os.kill(pid_search("app_main.py"))
        subprocess.run(["python", "mbox/app_main.py"])

app = QApplication(sys.argv)

logout()

sys.exit(app.exec_())
