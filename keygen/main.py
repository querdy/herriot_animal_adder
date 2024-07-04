
import sys
from datetime import timedelta

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from app.windows.main import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowIcon(QIcon('icons/key.png'))

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# ToDo pyinstaller --onefile -w --icon="icons/key.ico" --name="Herriot keygen" main.py
