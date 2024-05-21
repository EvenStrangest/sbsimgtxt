import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt


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
        hbox.addWidget(self.textEdit)

        # Load images and text
        self.directory = "G:/My Drive/Workplaces/Panta Rhei/Projects/Equashield first part/Param logs 2024MAY08/"
        self.files = sorted([f for f in os.listdir(self.directory) if f.endswith('.png')])
        self.currentIndex = 0
        self.loadContent(self.currentIndex)

        # Keyboard events
        self.keyPressEvent = self.changeImage

    def loadContent(self, index):
        if index < 0 or index >= len(self.files):
            return
        image_path = os.path.join(self.directory, self.files[index])
        text_path = image_path.replace('.png', '.txt')

        # Load and display the image
        self.imageLabel.setPixmap(QPixmap(image_path).scaled(768, 1366, Qt.KeepAspectRatio))

        # Load and display the text
        if os.path.exists(text_path):
            with open(text_path, 'r') as file:
                self.textEdit.setPlainText(file.read())
        else:
            self.textEdit.setPlainText("")

    def changeImage(self, event):
        if event.key() == Qt.Key_PageUp:
            self.saveText()
            self.currentIndex = (self.currentIndex - 1) % len(self.files)
            self.loadContent(self.currentIndex)
        elif event.key() == Qt.Key_PageDown:
            self.saveText()
            self.currentIndex = (self.currentIndex + 1) % len(self.files)
            self.loadContent(self.currentIndex)

    def saveText(self):
        text_path = os.path.join(self.directory, self.files[self.currentIndex]).replace('.png', '.txt')
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