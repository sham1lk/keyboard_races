import random
import sqlite3
import string
import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

# create a Window class
from helpers import get_ip, get_name
NAME = get_name().replace('-','_')
letters = string.ascii_lowercase
GAME_NAME= ''.join(random.choice(letters) for i in range(10))

from trainingWin import TrainingWin
from connect_game import ConnectGame
from create_game import CreateGame

training_window = None


class Window(QMainWindow):
    # constructor
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("New Game")
        self.main_menu()

    # method for components
    def main_menu(self):
        create_game = QPushButton("Create game", self)
        create_game.setGeometry(20, 380, 200, 50)
        create_game.clicked.connect(self.create_game)

        connect_to_game = QPushButton("Connect to the game", self)
        connect_to_game.setGeometry(285, 380, 200, 50)
        connect_to_game.clicked.connect(self.connect_to_game)

        training = QPushButton("Training", self)
        training.setGeometry(550, 380, 200, 50)
        training.clicked.connect(self.trainingBtn)

        # self.label = QLabel(self)
        # self.label.setObjectName("label")
        # self.label.setGeometry(20, 240, 260, 60)
        # self.label.setFont(QFont('Times', 15))
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setText("Your IP address: {}".format(get_ip()))

        nickname = QLabel(self)
        nickname.setObjectName("nickname")
        nickname.setGeometry(250, 300, 120, 30)
        nickname.setText("Your nickname: ")

        self.text_edit = QLineEdit()
        self.text_edit.setText(NAME)
        self.text_edit.setGeometry(370, 300, 180, 30)
        self.layout().addWidget(self.text_edit)

        pixmap = QPixmap('statics/image.jpg').scaled(400, 500, QtCore.Qt.KeepAspectRatio)

        # label = QLabel(self)
        # label.setPixmap(pixmap)
        # label.setGeometry(225, 50, 350, 200)

        picLabel = QLabel(self)
        picLabel.setObjectName("image")
        picLabel.setPixmap(pixmap)
        picLabel.setGeometry(225, 50, 350, 200)

        self.show()

    def create_game(self):
        self.w = CreateGame()

    def connect_to_game(self):
        self.w = ConnectGame()

    def trainingBtn(self):
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute(
        """REPLACE INTO users (name, progres, room) VALUES(?, ?, ?);""", (NAME,
                                                                0, GAME_NAME))
        conn.commit()
        self.w = TrainingWin()

    def hide_menu(self):
        pass


def start_app():
    # create the instance of our Window
    App = QApplication(sys.argv)
    style = """
        QWidget{
            background: #f2f2f2;
        }

        QLabel{
            font-family: Arial, Helvetica, sans-serif;
            color: #242424;
            font-size: 15px;
        }

        QLabel#progress_label, #pace_label, #lbll{
            font-family: Arial, Helvetica, sans-serif;
            color: #242424;
            font-size: 15px;
        }

        QLabel#sample_text{
            font-family: Arial, Helvetica, sans-serif;
            color: #242424;
            padding: 5px;
            font-size: 18px;
            border-style: solid;
            border: 2px solid #242424;
            border-radius: 10px;
        }

        QLabel#label, #image{
            font-family: Arial, Helvetica, sans-serif;
            color: #242424;
            padding: 5px;
            font-size: 14px;
            border-style: solid;
            border: 2px solid #242424;
            border-radius: 10px;
        }

        QLineEdit{
            font-family: Arial, Helvetica, sans-serif;
            padding: 5px;
            color: #f2f2f2;
            background-color: #242424;
            font-size: 14px;
            border: 2px solid #242424;
            border-radius: 10px;
        }

        QPushButton{
            font-family: Arial, Helvetica, sans-serif;
            padding: 5px;
            color: #242424;
            font-size: 14px;
            border-style: solid;
            border: 2px solid #242424;
            border-radius: 10px;
        }
        QPushButton:hover{
            color: #f2f2f2;
            background-color: #242424;
        }

        QProgressBar {
            border: 2px solid #242424;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #242424;
        }
    """
    App.setStyleSheet(style)

    window = Window()
    App.exec()
