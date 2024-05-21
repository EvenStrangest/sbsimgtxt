import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QSpacerItem, QSizePolicy, QShortcut
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QTextBlockFormat, QTextCursor
from PyQt5.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        if False:
            self.directory = "G:/My Drive/Workplaces/Panta Rhei/Projects/Equashield first part/Param logs 2024MAY08/"
            self.textbox_height = 720
            self.pixel_scaling = 1.0
            self.font_scaling = 1.0
        else:
            self.directory = r"G:\.shortcut-targets-by-id\17TZISjQGWmn48wdaugs_Hn8WmX7iyQVT\Panta Rhei\Projects\Equashield first part\Param logs 2024MAY08"
            self.textbox_height = 720
            # Adjust the scaling factors as needed
            self.pixel_scaling = 1.5
            self.font_scaling = 1.5

        self.initUI()

    def initUI(self):
        # Layout setup
        hbox = QHBoxLayout(self)
        self.setLayout(hbox)

        # Left image display
        self.imageLabel = QLabel(self)
        self.imageLabel.setFixedSize(int(self.pixel_scaling * 768), int(self.pixel_scaling * 1366))  # Set fixed size for the image display
        hbox.addWidget(self.imageLabel)

        # Right text edit, added to a separate vertical layout to move it lower
        textLayout = QVBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)  # Adjust the spacer size as needed
        textLayout.addItem(spacer)
        self.textEdit = QTextEdit(self)
        self.textEdit.setFixedSize(int(self.pixel_scaling * 768), int(self.pixel_scaling * self.textbox_height))  # Adjusted size to match layout requirements
        font = QFont("Consolas", int(self.font_scaling * 10))
        self.textEdit.setFont(font)
        textLayout.addWidget(self.textEdit)
        hbox.addLayout(textLayout)

        # Load images and text
        self.files = sorted([f for f in os.listdir(self.directory) if f.endswith('.png')])
        self.currentIndex = 0
        self.loadContent(self.currentIndex)

        # Setup shortcuts
        self.setupShortcuts()

    def adjustLineHeight(self):
        cursor = self.textEdit.textCursor()  # Get current cursor from the textEdit
        position = cursor.position()  # Save the current cursor position

        # Set up the block format for fixed line height
        block_format = QTextBlockFormat()
        block_format.setLineHeight(int(self.pixel_scaling * 17), QTextBlockFormat.FixedHeight)

        # Apply block format to the entire document without changing the cursor selection
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(block_format)
        cursor.clearSelection()  # Clear any selection

        # Restore the cursor to its original position
        cursor.setPosition(position)
        self.textEdit.setTextCursor(cursor)

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
        self.imageLabel.setPixmap(QPixmap(image_path).scaled(int(self.pixel_scaling * 768), int(self.pixel_scaling * 1366), Qt.KeepAspectRatio))

        # Load and display the text
        if os.path.exists(text_path):
            with open(text_path, 'r') as file:
                self.textEdit.setPlainText(file.read())
                self.adjustLineHeight()  # Adjust line height each time text is loaded
        else:
            self.textEdit.setPlainText("")
            self.adjustLineHeight()  # Adjust line height even if text is empty

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
