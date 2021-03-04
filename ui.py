import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

# create a Window class
from helpers import get_ip, get_name
from trainingWin import TrainingWin

training_window = None

class Window(QMainWindow):
    # constructor
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100,800, 600)
        self.setWindowTitle("New Game")
        self.main_menu()


    # method for components
    def main_menu(self):
        create_game = QPushButton("Create game", self)
        create_game.setGeometry(20, 380, 200, 50)
        create_game.clicked.connect(self.create_game)
        create_game.setFont(QFont('Times', 15))

        connect_to_game = QPushButton("Connect to the game", self)
        connect_to_game.setGeometry(285, 380, 200, 50)
        connect_to_game.clicked.connect(self.connect_to_game)
        connect_to_game.setFont(QFont('Times', 15))

        training = QPushButton("Training", self)
        training.setGeometry(550, 380, 200, 50)
        training.clicked.connect(self.trainingBtn)
        training.setFont(QFont('Times', 15))

        self.label = QLabel(self)
        self.label.setGeometry(20, 240, 260, 60)
        self.label.setFont(QFont('Times', 15))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Your IP address: {}".format(get_ip()))
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "color : black;"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")        

        nickname = QLabel(self)
        nickname.setGeometry(20, 100, 120, 25)
        nickname.setFont(QFont('Times', 15))
        nickname.setText("Your nickname: ")
        nickname.setStyleSheet("QLabel"
                              "{"
                              "color : black;"
                              "border : 3px solid black;"
                              "background : white;"
                              "}")

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(get_name())
        self.text_edit.setGeometry(140, 100, 140, 25)
        self.text_edit.setFont(QFont('Times', 15))
        self.layout().addWidget(self.text_edit)

        pixmap = QPixmap('statics/image.jpg').scaled(400, 500, QtCore.Qt.KeepAspectRatio)
        
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(400, 100, 350, 200)
        # self.layout().addWidget(label)
    
        self.show()

    def create_game(self):
        # self.nickname = self.text_edit.toPlainText()
        self.label.setText("Create game")


    def connect_to_game(self):
        self.label.setText("Connect game")

    def trainingBtn(self):
        self.label.setText("Training")
        self.w = TrainingWin()


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
