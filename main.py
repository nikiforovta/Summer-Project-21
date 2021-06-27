import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox

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
        pixmap = QPixmap(self.image_path)
        self.resize(pixmap.width(), pixmap.height())
        self.label.setPixmap(QPixmap(pixmap))
        # Активация кнопки вызова модели
        if not self.btn2.isEnabled():
            self.btn2.setEnabled(True)

    def print_class(self):
        # Получения отсортированного словаря вида "порода" : "вероятность"
        breeds = dict(sorted(classification(self.image_path).items(), key=lambda x: x[1], reverse=True))
        # Информационное диалоговое окно
        msg = QMessageBox()
        msg.setWindowTitle("I think it is")
        output = ""
        for k, v in breeds.items():
            if v > 0.01:
                output += f"{100 * v:.2f}%\t\t{str.replace(k, '_', ' ').title()}\n"
        msg.setText(output)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
