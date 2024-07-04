import sys

from PyQt6.QtWidgets import QApplication

from app.windows.main import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# ToDo pyinstaller --onefile -w --icon="icons/cow.ico" --name="Herriot animal registration" main.py
