from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QWidget, QStatusBar, QGridLayout

from app.windows.log import Log


class GroupRegister(QWidget):
    def __init__(self, log_window: Log, status_bar: QStatusBar, parent=None):
        super().__init__(parent)

        self.log_window = log_window
        self.status_bar = status_bar
        self.thread_pool = QThreadPool()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
