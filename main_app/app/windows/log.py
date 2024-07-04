from PyQt6.QtWidgets import QWidget, QFrame, QGridLayout

from app.windows.base import CustomPlainTextEdit


class Log(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()

        self.text_browser = CustomPlainTextEdit()
        self.text_browser.setReadOnly(True)
        self.text_browser.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(self.text_browser, 1, 1, 1, 1)
        self.setLayout(layout)

    def write(self, message):
        self.text_browser.write(message)

    def rewrite(self, message):
        self.text_browser.rewrite(message)

    def write_html(self, message):
        self.text_browser.write_html(message)

    def flush(self):
        self.text_browser.flush()
