from datetime import datetime, timedelta

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.uic.properties import QtGui, QtCore

from tasks import send_progress
from trainingWin import TrainingWin
from ui import NAME


class ConnectGame(QWidget):
    # constructor
    def __init__(self):
        super().__init__()
        self.wgtW = 800
        self.wgtH = 600
        self.setGeometry(100, 100, self.wgtW, self.wgtH)
        self.setWindowTitle("New Game")

        room_name = QLabel(self)
        room_name.setGeometry(20, 100, 120, 30)
        room_name.setText("Room Name: ")

        self.create_game = QPushButton("Connect game", self)
        self.create_game.setGeometry(20, 380, 200, 50)
        self.create_game.clicked.connect(self.connect)
        self.create_game.setFont(QFont('Times', 15))

        self.qle = QLineEdit(self)
        self.qle.move(150, 100)
        self.qle.textChanged[str].connect(self.onChanged)
        self.show()

    def onChanged(self):
        self.show()

    def connect(self):
        send_progress.apply_async(
            [NAME, 0, self.qle.text()])
        self.close()
        self.w = TrainingWin(training=False)
