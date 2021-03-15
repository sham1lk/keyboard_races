import random
import sqlite3

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, \
    QHBoxLayout, QFormLayout, QGridLayout

sample_text = [
    "In some natures there are no half-tones;\nnothing but raw primary colours. John Bodman\nwas a man who was always at one extreme or the other",
    "When and where, it matters not now to\nrelate--but once upon a time as I was\npassing through a thinly peopled district\nof country, night came down upon me, almost unawares.",
    "Some women had risen, in order to get\nnearer to him, and were standing with their\neyes fastened on the clean-shaven face\nof the judge, who was saying such weighty things",
    "Conradin hated her with a desperate sincerity\nwhich he was perfectly able to mask.",
    "The man held a double-barrelled gun cocked in his\nhand, and screwed up his eyes in the direction\nof his lean old dog who was running on ahead sniffing the bushes"
]


class CreateGame(QWidget):
    # constructor
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())
        self.wgtW = 800
        self.wgtH = 600
        self.setGeometry(100, 100, self.wgtW, self.wgtH)
        self.setWindowTitle("New Game")

        room_name = QLabel(self)
        room_name.setGeometry(20, 100, 120, 30)
        room_name.setText("Room Name: ")

        create_game = QPushButton("Create game", self)
        create_game.setGeometry(20, 380, 200, 50)
        create_game.clicked.connect(self.create_game)
        create_game.setFont(QFont('Times', 15))

        self.qle = QLineEdit(self)
        self.qle.move(150, 100)
        self.qle.textChanged[str].connect(self.onChanged)

        room_text = QLabel(self)
        room_text.setGeometry(280, 100, 120, 30)
        room_text.setText("Text to play:")

        self.text = QLineEdit(self)
        self.text.setGeometry(400, 100, 350, 350)
        self.text.textChanged[str].connect(self.onChanged)

        self.show()

    def onChanged(self):
        self.show()

    def create_game(self):
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute("""DROP table IF EXISTS game;""")
        cur.execute("""CREATE TABLE game(
            name TEXT PRIMARY KEY,
            text TEXT);
        """)
        text = self.text.text() or sample_text[
            random.randint(0, len(sample_text))]
        cur.execute(
            """INSERT INTO game (name, text) VALUES(?, ?);""",
            (self.qle.text(), text))
        conn.commit()
