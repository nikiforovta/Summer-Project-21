import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QGridLayout

from classification import classification, init_classification


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Вместо этого пустого поля будет добавлено изображение, выбранное пользователем
        self.label = QLabel("")
        # Кнопка для открытия изображения
        self.btn1 = QPushButton("Open Image")
        # Кнопка для вызова модели
        self.btn2 = QPushButton("Guess the Breed")
        self.title = "DBC"
        self.image_path = ""
        self.top = 200
        self.left = 500
        # Изначальные размеры отрисовываемого экрана
        self.width = 256
        self.height = 256

        self.result = QWidget()
        self.standard = QWidget()
        self.breed_to_show = ""

        self.init_window()

    def init_window(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)
        # При запуске приложения кнопка вызова модели неактивна
        self.btn2.setEnabled(False)
        # Подключение методов к кнопкам
        self.btn1.clicked.connect(self.get_image)
        self.btn2.clicked.connect(self.print_class)
        self.setLayout(vbox)
        # Инициализация модели
        init_classification()
        self.show()

    def get_image(self):
        # Открытие окна выбора изображения
        fname = QFileDialog.getOpenFileName(self, 'Open File', './', "Image (*.png *.jpg *jpeg)")
        self.image_path = fname[0]
        pixmap = QPixmap(self.image_path).scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(QPixmap(pixmap))
        # Активация кнопки вызова модели
        if not self.btn2.isEnabled():
            self.btn2.setEnabled(True)
        self.result = QWidget()

    def print_class(self):
        # Получения отсортированного словаря вида "порода" : "вероятность"
        breeds = dict(sorted(classification(self.image_path).items(), key=lambda x: x[1], reverse=True))
        self.result.setWindowTitle("I think it is")
        self.result.setWindowIcon(QtGui.QIcon("icon.png"))
        self.result.setGeometry(600, 300, 256, 256)
        msgbox = QGridLayout()
        i = 0
        for k, v in breeds.items():
            if v > 0.01:
                msgbox.addWidget(QLabel(f"{100 * v:.2f}%"), i, 0)
                btn_breed = QPushButton(k)
                btn_breed.clicked.connect(self.show_match)
                msgbox.addWidget(btn_breed, i, 1)
                i += 1
        self.result.setLayout(msgbox)
        self.result.show()

    def show_match(self):
        self.standard = QWidget()
        self.standard.setGeometry(850, 300, 220, 220)
        breed = self.sender().text()
        imgbox = QVBoxLayout()
        breed_pixmap = QPixmap(f"./standard/{breed}.jpg")
        breed_label = QLabel("")
        breed_label.setPixmap(QPixmap(breed_pixmap))
        imgbox.addWidget(breed_label)
        self.standard.setLayout(imgbox)
        self.standard.resize(breed_pixmap.width(), breed_pixmap.height())
        self.standard.setWindowTitle(f"Breed: {breed}")
        self.standard.setWindowIcon(QtGui.QIcon("icon.png"))
        self.standard.show()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
