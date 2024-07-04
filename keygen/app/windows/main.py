from datetime import timedelta, datetime

import machineid
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QGridLayout, QMainWindow, QWidget, QLineEdit, QLabel, QCheckBox, QVBoxLayout, QPushButton, \
    QComboBox, QFrame

from app.license_service import MachineJWT
from app.windows.base import CustomPlainTextEdit

districts: dict[str, str] = {
    "a309e4ce-2f36-4106-b1ca-53e0f48a6d95": "Пермь",
    "4f07ade1-1415-44c8-bed9-e851f1ef558d": "Александровск",
    "4ffcde97-05e9-4a6e-bd51-3a984b41b7bd": "Березники",
    "edeaf203-1bc3-4fe1-b3ed-15eb89978783": "Гремячинск",
    "1dc365d3-60b1-41ea-a3b3-1c599024cf30": "Губаха",
    "230c2f4d-fd9d-46fc-8bbd-b8de26810790": "Добрянка",
    "cc8b9eb5-bd4e-4472-8314-f889e8a6679c": "Кизел",
    "d36590ad-0286-44a2-876d-7732deee4234": "Кудымкар",
    "73e5113d-949a-4a9e-8e44-6eae9ef93747": "Кунгур",
    "5d7c95a5-a4d7-4fb4-9774-93e527636a9e": "Лысьва",
    "8b698775-fe5e-4fc0-9f0d-272855d82d15": "Соликамск",
    "06d7a6d6-8f57-4e5a-b698-2bc44c92bb84": "Чайковский",
    "784b1911-182d-476b-a4ad-0f3fa1ef7777": "Чусовой",
    "0810dccb-7114-4d33-9454-50b00433eb1b": "Бардымский район",
    "57e3f364-d709-44a4-a81f-c9ea68778fd0": "Березовский район",
    "76561b13-cc96-478c-9266-bc69ec254776": "Большесосновский район",
    "c3700ef0-0a85-4032-947c-009f956fd754": "Верещагинский район",
    "d336561f-cc98-4742-9f7b-52d99c78463e": "Гайнский район",
    "b6c85a2d-c0ec-4030-a306-4ca7bdcd25f4": "Горнозаводский район",
    "3afa40f2-8169-4006-a5c4-33ace0510d7f": "Еловский район",
    "a80bf180-06e3-4b38-971c-ecef8b417337": "Ильинский район",
    "44166947-11b9-4a1b-a1bf-6e9cba64299d": "Карагайский район",
    "c787b918-d201-408b-abb9-84d53befc6a5": "Кишертский район",
    "6e850977-64c1-49ac-a405-8ff2d77fa219": "Косинский район",
    "a4b9d248-dec4-4686-b4bc-d3b0d8fd9be6": "Кочевский район",
    "e4172d66-d08e-4eda-a274-c47119c30470": "Красновишерский район",
    "1ffa3973-279c-4bcd-a9fc-ece8c7d1039e": "Краснокамский район",
    "6fe17476-90db-4bbf-af4f-e33564751f95": "Кудымкарский район",
    "189875b0-b84b-4980-a125-5a0581f5197e": "Куединский район",
    "1f81a925-75ee-4fa2-87b1-9de26a2813ed": "Кунгурский район",
    "fa41d32f-22b5-4436-bddd-c2ec035377c6": "Нытвенский район",
    "2ddaf37d-e4ea-4748-b6b8-943854f37a0f": "Октябрьский район",
    "5ca82a07-403e-48aa-8fa8-a00277123e46": "Ординский район",
    "60dd742a-3dc9-4ab1-9a22-12c19efdb340": "Осинский район",
    "e7012a7a-e7de-4306-8f52-aabeaf82f178": "Оханский район",
    "2e82fea7-7e6f-4c8a-849f-57140f80c7f3": "Очерский район",
    "7dd380b3-ce33-4280-934f-a4265a07803b": "Пермский район",
    "9eea0415-ab1c-4b49-bd9d-aa04ea23d4e9": "Сивинский район",
    "db4332aa-5444-4c77-a364-541563e0bb1d": "Соликамский район",
    "9460a26c-a2b9-4cb2-9e0e-ddc9022b0ecb": "Суксунский район",
    "a266fff5-5817-4d3b-95dd-c447144f02d1": "Уинский район",
    "7f21b9b5-1f39-44ad-8ce4-6e186e8389ce": "Усольский район",
    "0e9750c7-9f8c-4e23-b996-9a7bff46bb2c": "Частинский район",
    "4f092f1f-8ebf-4ea4-8f01-a75cbcf1d43f": "Чердынский район",
    "75550fdb-56e3-44d5-a4c4-75ab2cb53e83": "Чернушинский район",
    "03547d69-de22-4781-b728-e0823fcdb5f3": "Юрлинский район",
    "f8523e08-3e73-4ba1-b1a2-4bdaf1e8b82f": "Юсьвинский район",
}


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(720, 480)
        self.setWindowTitle("Herriot: keygen")

        self.added_districts: set[str] = set()

        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_layout.setVerticalSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.machine_id_label = QLabel("ID Устройства:")
        self.machine_id_edit = QLineEdit(machineid.id())
        self.main_layout.addWidget(self.machine_id_label, 0, 0, 1, 1)
        self.main_layout.addWidget(self.machine_id_edit, 0, 1, 1, 5)

        self.expiry_label = QLabel("Срок действия (дн.):")
        self.expiry_edit = QLineEdit()
        self.main_layout.addWidget(self.expiry_label, 1, 0, 1, 1)
        self.main_layout.addWidget(self.expiry_edit, 1, 1, 1, 5)

        self.checkbox_layout = QVBoxLayout()
        self.main_layout.addLayout(self.checkbox_layout, 2, 0)

        self.districts_text_browser = CustomPlainTextEdit()
        self.districts_text_browser.setReadOnly(True)
        self.districts_text_browser.setFrameShape(QFrame.Shape.NoFrame)
        self.districts_text_browser.setMaximumHeight(100)
        self.main_layout.addWidget(self.districts_text_browser, 4, 0, 1, 6)

        self.district_combobox = QComboBox()
        for key, value in districts.items():
            self.district_combobox.addItem(value, key)
        self.main_layout.addWidget(self.district_combobox, 3, 0, 1, 1)

        self.add_district_button = QPushButton()
        self.add_district_button.setText('Добавить')
        self.add_district_button.clicked.connect(self.add_district)
        self.main_layout.addWidget(self.add_district_button, 3, 1, 1, 1)

        self.clear_district_button = QPushButton()
        self.clear_district_button.setText('Очистить')
        self.clear_district_button.clicked.connect(self.clear_districts)
        self.main_layout.addWidget(self.clear_district_button, 3, 2, 1, 1)

        self.generate_button = QPushButton()
        self.generate_button.setText('Сгенерировать')
        self.generate_button.clicked.connect(self.generate_license_key)
        self.main_layout.addWidget(self.generate_button, 5, 0, 1, 1)

        self.machine_id_label = QLabel("Ключ продукта:")
        self.main_layout.addWidget(self.machine_id_label, 6, 0, 1, 1)

        self.machine_id_label = QLabel("Проверка ключа:")
        self.main_layout.addWidget(self.machine_id_label, 8, 0, 1, 1)

        self.license_key_text_browser = CustomPlainTextEdit()
        self.license_key_text_browser.setReadOnly(True)
        self.license_key_text_browser.setFrameShape(QFrame.Shape.NoFrame)
        self.license_key_text_browser.setMaximumHeight(100)
        self.main_layout.addWidget(self.license_key_text_browser, 7, 0, 1, 6)

        self.test_license_key_text_browser = CustomPlainTextEdit()
        self.test_license_key_text_browser.setReadOnly(True)
        self.test_license_key_text_browser.setFrameShape(QFrame.Shape.NoFrame)
        self.test_license_key_text_browser.setMaximumHeight(100)
        self.main_layout.addWidget(self.test_license_key_text_browser, 9, 0, 1, 6)

        self.main_widget.setLayout(self.main_layout)
        self.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def add_district(self):
        current_district_guid = self.district_combobox.currentData()
        if current_district_guid not in self.added_districts:
            self.added_districts.add(current_district_guid)
            self.districts_text_browser.write(
                f"{self.district_combobox.currentText()} - {self.district_combobox.currentData()}\n"
            )

    def clear_districts(self):
        self.added_districts.clear()
        self.districts_text_browser.clear()

    def generate_license_key(self):
        try:
            expiry = float(self.expiry_edit.text().strip())
            machine_id = self.machine_id_edit.text().strip()
            license_key = MachineJWT(machine_id).encode(
                exp=timedelta(days=expiry),
                district=list(self.added_districts)
            )
            self.license_key_text_browser.clear()
            self.license_key_text_browser.write(license_key)
            decoded_license_key = MachineJWT(machine_id).decode(license_key)
            decoded_license_key["exp"] = datetime.fromtimestamp(decoded_license_key["exp"])
            self.test_license_key_text_browser.clear()
            self.test_license_key_text_browser.write(str(decoded_license_key))
        except ValueError as err:
            print(err)
