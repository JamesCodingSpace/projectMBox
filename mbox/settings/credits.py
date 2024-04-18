import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt5 Beispiel')

        # Ein Layout erstellen, um das Label zu platzieren
        layout = QVBoxLayout(self)

        # Label erstellen und Text setzen
        self.label = QLabel('Mbox! made by \nMadeleine Reuther and Tom Vogel!', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Fenstergröße an den Text anpassen
        self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
