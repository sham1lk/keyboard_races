import random
import sqlite3
from datetime import datetime, timedelta

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton

from helpers import sample_text
from trainingWin import TrainingWin
from ui import NAME


class CreateGame(QWidget):
    # constructor
    def __init__(self):
        super().__init__()
        self.wgtW = 800
        self.wgtH = 600
        self.setGeometry(100, 100, self.wgtW, self.wgtH)
        self.setWindowTitle("New Game")

        room_name = QLabel(self)
        room_name.setGeometry(275, 220, 100, 30)
        room_name.setText("Room Name: ")

        self.qle = QLineEdit(self)
        self.qle.setGeometry(375, 220 ,150, 30)
        self.qle.textChanged[str].connect(self.onChanged)

        self.text = QLineEdit(self)
        self.text.setGeometry(100, 275, 600, 50)
        self.text.setPlaceholderText("Here you can type your custom text or random text will be chosen")
        self.text.textChanged[str].connect(self.onChanged)

        create_game = QPushButton("Start game", self)
        create_game.setGeometry(300, 370, 200, 50)
        create_game.clicked.connect(self.create)
        create_game.setFont(QFont('Times', 15))

        self.show()

    def onChanged(self):
        self.show()

    def create(self):
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute("""DROP table IF EXISTS game;""")
        cur.execute("""CREATE TABLE game(
            name TEXT PRIMARY KEY,
            text TEXT,
            time timestamp);
        """)

        text = self.text.text() or sample_text[
            random.randint(0, len(sample_text)-1)]
        cur.execute(
            """INSERT INTO game (name, text, time) VALUES(?, ?, ?);""",
            (self.qle.text(), text, datetime.utcnow() + timedelta(0, 10)))
        conn.commit()

        cur.execute(
        """REPLACE INTO users (name, progres, room) VALUES(?, ?, ?);""", (NAME,
                                                                0, self.qle.text()))
        conn.commit()
        self.close()
        self.w = TrainingWin(training=False, creator=True)
