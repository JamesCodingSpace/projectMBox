import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget): # Öffnet kleines Fenster in dem die Credits angezeigt werden
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt5 Beispiel')
        layout = QVBoxLayout(self)

        self.label = QLabel('Mbox! made by \nMadeleine Reuther and Tom Vogel!', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
