import pandas as pd
from PyQt6 import QtGui
from PyQt6.QtCore import QMetaObject, Qt, Q_ARG, QAbstractTableModel
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QPlainTextEdit, QTableWidget


class CustomQTableWidget(QTableWidget):
    def set_color_to_row(self, row_idx: int, color: tuple[int, int, int]):
        for col_idx in range(self.columnCount()):
            try:
                self.item(row_idx, col_idx).setBackground(
                    QtGui.QColor(*color)
                )
            except AttributeError:
                continue

    def set_row_and_column_count(self, shape: tuple[int, int]):
        self.setRowCount(shape[0])
        self.setColumnCount(shape[1])


class CustomPlainTextEdit(QPlainTextEdit):
    def write(self, message):
        message = message.strip()
        if message:
            QMetaObject.invokeMethod(
                self,
                "appendPlainText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, message),
            )

    def rewrite(self, message):
        message = message.strip()
        if message:
            self.moveCursor(
                QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor
            )
            self.moveCursor(
                QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.MoveAnchor
            )
            self.moveCursor(
                QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor
            )
            self.textCursor().removeSelectedText()
            QMetaObject.invokeMethod(
                self,
                "appendPlainText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, message),
            )

    def write_html(self, message):
        message = message.strip()
        if message:
            QMetaObject.invokeMethod(
                self,
                "appendHtml",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, message),
            )

    def flush(self):
        QMetaObject.invokeMethod(self, "clear", Qt.ConnectionType.QueuedConnection)
