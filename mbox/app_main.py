import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QTextEdit, QVBoxLayout, QWidget, QListWidgetItem, QLabel, QAction, QToolBar, QMenu
import subprocess

# Dummy-Daten für E-Mail-Liste und E-Mail-Inhalt
emails = [("Absender 1", "Betreff 1", "Inhalt der E-Mail 1", "01.04.2024"), 
          ("Absender 2", "Betreff 2", "Inhalt der E-Mail 2", "02.04.2024"), 
          ("Absender 3", "Betreff 3", "Inhalt der E-Mail 3", "03.04.2024")]

class EmailClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-Mail Postfach")
        self.setGeometry(100, 100, 800, 600)

        self.create_toolbar()
        
        splitter = QSplitter(self)
        self.setCentralWidget(splitter)

        # Linkes Layout für Absender, Betreff und Sendedatum
        left_layout = QVBoxLayout()
        self.email_info = QLabel()
        left_layout.addWidget(self.email_info)

        # Rechte Spalte für E-Mail-Inhalt
        self.email_content = QTextEdit()
        splitter.addWidget(self.email_content)

        # Linke Spalte für E-Mail-Liste
        self.email_list = QListWidget()
        for sender, subject, _, _ in emails:
            item = QListWidgetItem(f"{sender}\n{subject}")
            self.email_list.addItem(item)
        self.email_list.itemSelectionChanged.connect(self.on_email_selected)
        left_layout.addWidget(self.email_list)

        # Widget für das linke Layout erstellen
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        # Setze das Verhältnis des Splitters (4:1)
        sizes = [self.width() // 5 * 4, self.width() // 5]  # 4 Teile für Inhalt, 1 Teil für Liste
        splitter.setSizes(sizes)

    def create_toolbar(self):
        self.toolbar = self.addToolBar("Toolbar")

        settings_menu = QMenu()
        logout_action = QAction("Abmelden", self)
        logout_action.triggered.connect(self.logout)
        settings_menu.addAction(logout_action)
        credits_action = QAction("Credits", self)
        credits_action.triggered.connect(self.show_credits)
        settings_menu.addAction(credits_action)

        settings_action = QAction("Einstellungen", self)
        settings_action.setMenu(settings_menu)
        self.toolbar.addAction(settings_action)

        new_email_action = QAction("E-Mail Schreiben", self)
        new_email_action.triggered.connect(self.write_email)
        self.toolbar.addAction(new_email_action)

        self.reply_action = QAction("Antworten", self)
        self.reply_action.setVisible(False)
        self.reply_action.triggered.connect(self.reply_email)
        self.toolbar.addAction(self.reply_action)

        self.forward_action = QAction("Weiterleiten", self)
        self.forward_action.setVisible(False)
        self.forward_action.triggered.connect(self.forward_email)
        self.toolbar.addAction(self.forward_action)

        self.delete_email_action = QAction("E-Mail Löschen", self)
        self.delete_email_action.triggered.connect(self.delete_email)
        self.delete_email_action.setVisible(False)  # Die Schaltfläche ist standardmäßig unsichtbar
        self.toolbar.addAction(self.delete_email_action)

    def write_email(self):
        print("Neue E-Mail schreiben")

    def reply_email(self):
        print("Antwort auf E-Mail verfassen")

    def forward_email(self):
        print("E-Mail weiterleiten")

    def delete_email(self):
        print("E-Mail löschen")

    def logout(self):
        subprocess.run(["python", "mbox/settings/logout.py"])

    def show_credits(self):
        print("Made by NAME, NAME, NAME, NAME; with help of") # DIALOG FENSTER HINZUFÜGEN

    def on_email_selected(self):
        # Funktion zum Anzeigen des ausgewählten E-Mail-Inhalts
        selected_item = self.email_list.currentItem()
        if selected_item:
            index = self.email_list.row(selected_item)
            sender, subject, content, sent_date = emails[index]
            email_info_text = f"Absender: {sender}\nBetreff: {subject}\nSendedatum: {sent_date}"
            self.email_info.setText(email_info_text)
            self.email_content.setPlainText(content)
            self.toolbar.removeAction(self.delete_email_action)
            self.toolbar.addAction(self.delete_email_action)
            self.reply_action.setVisible(True)
            self.forward_action.setVisible(True)
            self.delete_email_action.setVisible(True)


def main():
    app = QApplication(sys.argv)
    client = EmailClient()
    client.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
