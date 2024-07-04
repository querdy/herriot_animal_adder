from PyQt6.QtCore import QMetaObject, Q_ARG, Qt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QPlainTextEdit


class CustomPlainTextEdit(QPlainTextEdit):
    def write(self, message):
        message = message.strip()
        if message:
            QMetaObject.invokeMethod(self, "appendPlainText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, message))

    def rewrite(self, message):
        message = message.strip()
        if message:
            self.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
            self.moveCursor(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.MoveAnchor)
            self.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
            self.textCursor().removeSelectedText()
            QMetaObject.invokeMethod(self, "appendPlainText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, message))

    def write_html(self, message):
        message = message.strip()
        if message:
            QMetaObject.invokeMethod(self, "appendHtml", Qt.ConnectionType.QueuedConnection, Q_ARG(str, message))

    def flush(self):
        QMetaObject.invokeMethod(self, "clear", Qt.ConnectionType.QueuedConnection)
