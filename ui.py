import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

# create a Window class
from helpers import get_ip, get_name


class Window(QMainWindow):
    # constructor
    def __init__(self):
        super().__init__()

        # setting title
        self.main_menu()


    # method for components
    def main_menu(self):
        self.setGeometry(100, 100,
                         800, 600)
        self.setWindowTitle("New Game")
        create_game = QPushButton("Create game", self)
        connect_to_game = QPushButton("Connect to the game", self)
        create_game.setGeometry(100, 380, 200, 50)
        connect_to_game.setGeometry(500, 380, 200, 50)
        connect_to_game.clicked.connect(self.connect_to_game)
        create_game.clicked.connect(self.create_game)
        connect_to_game.setFont(QFont('Times', 15))
        create_game.setFont(QFont('Times', 15))
        self.label = QLabel(self)
        nickname = QLabel(self)
        nickname.setFont(QFont('Times', 15))
        nickname.setGeometry(20, 100, 145, 60)
        # setting geometry to the label
        self.label.setGeometry(20, 240, 260, 60)

        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")
        nickname.setStyleSheet("QLabel"
                              "{"
                              "border : 3px solid black;"
                              "background : white;"
                              "}")

        nickname.setText("Your nickname: ")

        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(QFont('Times', 15))
        self.label.setText("Your IP address: {}".format(get_ip()))
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(get_name())
        self.text_edit.setGeometry(165, 100, 115, 60)
        self.text_edit.setFont(QFont('Times', 15))
        self.layout().addWidget(self.text_edit)
        label = QLabel(self)
        pixmap = QPixmap('statics/image.jpg').scaled(400, 500, QtCore.Qt.KeepAspectRatio)

        label.setPixmap(pixmap)
        label.setGeometry(400, 100, 350, 200)
        self.layout().addWidget(label)
        self.show()

    def create_game(self):
        self.nickname = self.text_edit.toPlainText()


    def connect_to_game(self):
        self.label.setText("Connect game")

    def hide_menu(self):
        pass


# create pyqt5 app
App = QApplication(sys.argv)


def start_app():
    # create the instance of our Window
    window = Window()
    App.exec()
# start the app
# sys.exit(App.exec())
