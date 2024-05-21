import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QIcon, QKeySequence, QFont
from PyQt5.QtCore import Qt, QEvent


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout setup
        hbox = QHBoxLayout(self)
        self.setLayout(hbox)

        # Left image display
        self.imageLabel = QLabel(self)
        self.imageLabel.setFixedSize(768, 1366)  # Set fixed size for the image display
        hbox.addWidget(self.imageLabel)

        # Right text edit
        self.textEdit = QTextEdit(self)
        self.textEdit.setFixedSize(768, 1366)
        font = QFont("Consolas", 16)  # Set font type and size
        self.textEdit.setFont(font)
        hbox.addWidget(self.textEdit)

        # Load images and text
        self.directory = "G:/My Drive/Workplaces/Panta Rhei/Projects/Equashield first part/Param logs 2024MAY08/"
        self.files = sorted([f for f in os.listdir(self.directory) if f.endswith('.png')])
        self.currentIndex = 0
        self.loadContent(self.currentIndex)

        # Setup shortcuts
        self.setupShortcuts()

    def setupShortcuts(self):
        QShortcut(QKeySequence(Qt.Key_PageUp), self, activated=self.previousImage)
        QShortcut(QKeySequence(Qt.Key_PageDown), self, activated=self.nextImage)

    def previousImage(self):
        if self.currentIndex > 0:
            self.saveText()
            self.currentIndex -= 1
            self.loadContent(self.currentIndex)

    def nextImage(self):
        if self.currentIndex < len(self.files) - 1:
            self.saveText()
            self.currentIndex += 1
            self.loadContent(self.currentIndex)

    def loadContent(self, index):
        if index < 0 or index >= len(self.files):
            return
        image_path = os.path.join(self.directory, self.files[index])
        text_path = os.path.join(self.directory, 'generated', self.files[self.currentIndex]).replace('.png', '_central_table.txt')

        # Load and display the image
        self.imageLabel.setPixmap(QPixmap(image_path).scaled(768, 1366, Qt.KeepAspectRatio))

        # Load and display the text
        if os.path.exists(text_path):
            with open(text_path, 'r') as file:
                self.textEdit.setPlainText(file.read())
        else:
            self.textEdit.setPlainText("")

        # Set window title to the active image filename
        self.setWindowTitle(os.path.basename(self.files[index]))

    def saveText(self):
        text_path = os.path.join(self.directory, 'generated', self.files[self.currentIndex]).replace('.png', '_central_table.txt')
        with open(text_path, 'w') as file:
            file.write(self.textEdit.toPlainText())


def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.setWindowTitle('Image and Text Viewer')
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
