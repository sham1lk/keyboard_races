import sqlite3

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel

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
        room_name.setGeometry(275, 250, 100, 30)
        room_name.setText("Room Name: ")

        self.create_game = QPushButton("Connect game", self)
        self.create_game.setGeometry(300, 350, 200, 50)
        self.create_game.clicked.connect(self.connect)
        self.create_game.setFont(QFont('Times', 15))

        self.qle = QLineEdit(self)
        # self.qle.move(150, 100)
        self.qle.setGeometry(375, 250, 150, 30)
        self.qle.textChanged[str].connect(self.onChanged)
        self.show()

    def onChanged(self):
        self.show()

    def connect(self):
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute("""DROP table IF EXISTS game;""")
        cur.execute("""CREATE TABLE game(
            name TEXT PRIMARY KEY,
            text TEXT,
            time timestamp);
        """)
        conn.commit()
        cur.execute(
            """REPLACE INTO users (name, room, progres) VALUES(?, ?, ?);""",
            (NAME, self.qle.text(), 0))
        conn.commit()
        send_progress.apply_async(
            [NAME, self.qle.text(), 0])
        self.close()
        self.w = TrainingWin(training=False)
