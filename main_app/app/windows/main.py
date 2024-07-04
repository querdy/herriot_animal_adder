import machineid
import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, Qt, QObject, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTableView, QTabWidget, QGridLayout, QWidget

from app.license_service import load_license, MachineJWT, TokenError
from app.vetis.main import Vetis
from app.windows.group_register import GroupRegister
from app.windows.individual_register import IndividualRegister
from app.windows.log import Log
from app.windows.report import Report
from app.windows.service import Service


class MainSignals(QObject):
    vetis_initialized = pyqtSignal(bool)
    license_checked = pyqtSignal(bool)
    allowed_districts_received = pyqtSignal(list)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("Herriot: учёт животных")
        self.signals = MainSignals()
        self.signals.license_checked.connect(self.license_checked)
        self.signals.vetis_initialized.connect(self.api_data_checked)

        self.verifiable_data = {
            "license": False,
            "api_data": False,
        }

        self.is_license_enabled = False
        self.is_api_data_correctness = False

        self.main_tab_widget = QTabWidget()

        self.log_window = Log(self)
        self.main_tab_widget.addTab(
            IndividualRegister(self.log_window, self.statusBar(), self),
            "Индивидуальная регистрация",
        )
        self.main_tab_widget.setTabIcon(0, QIcon("icons/cow.png"))
        self.main_tab_widget.setTabEnabled(0, False)
        self.main_tab_widget.addTab(
            GroupRegister(self.log_window, self.statusBar(), self),
            "Групповая регистрация",
        )
        self.main_tab_widget.setTabIcon(1, QIcon("icons/habitat.png"))
        self.main_tab_widget.setTabEnabled(1, False)

        self.main_tab_widget.addTab(
            Service(self.log_window, self.statusBar(), parent=self), "Сервис"
        )
        self.main_tab_widget.setTabIcon(2, QIcon("icons/gear.png"))

        self.main_tab_widget.addTab(Report(self.log_window, self.statusBar(), parent=self), "Отчеты")
        self.main_tab_widget.setTabEnabled(3, False)

        self.log_tab_widget = QTabWidget(self)
        self.log_tab_widget.addTab(self.log_window, "Инфо")

        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.main_tab_widget, 0, 0, 5, 1)
        main_layout.addWidget(self.log_tab_widget, 5, 0, 2, 1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def license_checked(self, value: bool):
        self.verifiable_data["license"] = value
        if all(self.verifiable_data.values()):
            self.main_tab_widget.setTabEnabled(0, True)
            self.main_tab_widget.setCurrentIndex(0)
        else:
            self.main_tab_widget.setTabEnabled(0, False)
            self.main_tab_widget.setCurrentIndex(2)

    def api_data_checked(self, value: bool):
        self.verifiable_data["api_data"] = value
        if value:
            self.setWindowTitle(f"Herriot: учёт животных ({Vetis.initiator()})")
        else:
            self.setWindowTitle(f"Herriot: учёт животных")
        if all(self.verifiable_data.values()):
            self.main_tab_widget.setTabEnabled(0, True)
            self.main_tab_widget.setCurrentIndex(0)
        else:
            self.main_tab_widget.setTabEnabled(0, False)
            self.main_tab_widget.setCurrentIndex(2)
