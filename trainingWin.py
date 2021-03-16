import sqlite3
import time
from datetime import datetime, timedelta

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import random
from tasks import send_progress, app, pregame_communication
from ui import NAME

conn = sqlite3.connect('orders.db')
cur = conn.cursor()


def get_progres(name):
    try:
        cur.execute("SELECT progres FROM users where name=?", (name,))
        return int(cur.fetchall()[0][0])
    except:
        return 0


def get_game(name):
    cur.execute("SELECT room FROM users where name=?", (name,))
    game = cur.fetchall()
    if game:
        cur.execute("SELECT * FROM game where name=?", (game[0][0],))
        return cur.fetchall()
    else:
        return False

def string_to_time(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S.%f')

class TrainingWin(QWidget):
    # constructor

    def __init__(self, training=True, creator=False):
        super().__init__()
        self.sample_text = []
        self.sample_text.append(
            "In some natures there are no half-tones;\nnothing but raw primary colours. John Bodman\nwas a man who was always at one extreme or the other")
        self.sample_text.append(
            "When and where, it matters not now to\nrelate--but once upon a time as I was\npassing through a thinly peopled district\nof country, night came down upon me, almost unawares.")
        self.sample_text.append(
            "Some women had risen, in order to get\nnearer to him, and were standing with their\neyes fastened on the clean-shaven face\nof the judge, who was saying such weighty things")
        self.sample_text.append(
            "Conradin hated her with a desperate sincerity\nwhich he was perfectly able to mask.")
        self.sample_text.append(
            "The man held a double-barrelled gun cocked in his\nhand, and screwed up his eyes in the direction\nof his lean old dog who was running on ahead sniffing the bush")
        self.game_text = self.sample_text[random.randint(0, len(self.sample_text) - 1)]
        self.game_name = 'training'
        self.start_time = datetime.utcnow()
        if creator:
            game = get_game(NAME)
            game = game[0]
            self.game_name = game[0]
            self.game_text = game[1]
            self.start_time = string_to_time(game[2])
            k = 0
            while k<10:
                print(self.start_time, datetime.utcnow() - timedelta(0, 5))
                pregame_communication.apply_async(
                    [self.game_name, self.game_text, self.start_time])
                k+=1
                time.sleep(1)
        elif not training:
            game = get_game(NAME)
            while not game:
                time.sleep(1)
            game = game[0]
            self.game_name = game[0]
            self.game_text = game[1]
            self.start_time = game[2]

        self.sampleTxt = QLabel(self)
        self.qle = QLineEdit(self)
        self.lbl = QLabel(self)

        # TODO: SQL player amount
        self.playerAmount = 3
        self.pbar = []
        self.plbl = []
        self.pacelbl = []
        self.finished = []
        for i in range(self.playerAmount):
            self.pbar.append(QProgressBar(self))
            self.plbl.append(QLabel(self))
            self.pacelbl.append(QLabel(self))
            self.finished.append(0)

        if training:
            self.restart = QPushButton("Restart", self)
            self.restart.setGeometry(550, 20, 200, 50)
            self.restart.clicked.connect(self.restartBtn)

        self.reset()


    def reset(self):
        self.idx = random.randint(0, len(self.sample_text) - 1)
        self.stxtLen = len(self.sample_text[self.idx])
        self.stxtSpace = self.sample_text[self.idx].count(' ')
        self.splitted = self.sample_text[self.idx].split()

        self.wgtW = 800
        self.wgtH = 600
        self.setGeometry(100, 100, self.wgtW, self.wgtH)
        self.setWindowTitle("New Game")

        self.stxtLen = len(self.game_text)
        self.stxtSpace = self.game_text.count(' ')
        self.splitted = self.game_text.split()
        self.training_ui()
        self.correct_words = 0
        self.started = False
        self.start_time = 0.0;
        self.end_time = 0.0;
        self.cwPtr = 0

        self.training_ui()
        

    def training_ui(self):
        self.sampleTxt.setObjectName("sample_text")
        self.sampleTxt.setGeometry(285, 140, 260, 60)
        self.sampleTxt.setAlignment(Qt.AlignCenter)
        self.sampleTxt.setText(self.game_text)
        self.sampleTxt.adjustSize()
        h1 = int(self.sampleTxt.height() * 1.6)
        w1 = int(self.sampleTxt.width() * 1.3)
        stx = (self.wgtW - w1) / 2
        sty = (self.wgtH - h1) / 5
        self.sampleTxt.setGeometry(stx, sty, w1, h1)

        qlw = 140
        qlh = 25
        w2 = int(stx + (w1 - qlw) / 2)
        
        self.qle.clear()
        self.qle.setGeometry(w2, sty + h1 + 25, qlw, qlh + 5)
        self.qle.textChanged[str].connect(self.onChanged)

        lbly = sty + h1 + 30
        
        self.lbl.setObjectName("lbll")
        self.lbl.setText("0")
        self.lbl.setGeometry(w2 + qlw + 20, lbly, 30, qlh)

        pbrW = 500
        pbrx = (self.wgtW - pbrW) / 2
        pbry = lbly + 120
        

        for i in range(self.playerAmount):
            self.pbar[i].setTextVisible(False);
            self.pbar[i].setValue(0)
            self.pbar[i].setGeometry(pbrx, pbry, pbrW, qlh - 10)

            plby = pbry - 25

            self.plbl[i].setObjectName("progress_label" + str(i))
            self.plbl[i].setGeometry(pbrx + 5, plby, 30, qlh)
            self.plbl[i].setText("0%")

            self.pacelbl[i].setObjectName("pace_label" + str(i))
            self.pacelbl[i].setText("")
            self.pacelbl[i].setGeometry(pbrx + pbrW - 100, plby, 50, qlh)

            pbry += 50



        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)

        self.show()


    def time(self):
        for i in range(self.playerAmount):
            self.pbar[i].setValue(get_progres(NAME))
            self.plbl[i].setText(str(get_progres(NAME)) + "%")
            self.plbl[i].adjustSize()

            if self.started and self.finished[i]==0:
                if self.pbar[i].value() > 99:
                    self.end_time = time.perf_counter()
                    pace = 60 * ((self.stxtLen - self.stxtSpace) / (self.end_time - self.start_time))
                    pace = str(round(pace, 2))
                    self.pacelbl[i].setText(pace + " sym/min") 
                    self.pacelbl[i].adjustSize()
                    self.finished[i] = 1


    def onChanged(self, text):
        if not self.started:
            self.start_time = time.perf_counter()
            self.started = True

        if self.correct_words != len(self.splitted):
            if text == (self.splitted[self.correct_words] + " "):
                self.qle.clear()

                tmp = '_' * len(self.splitted[self.correct_words])
                tmp = self.game_text[:self.cwPtr] + tmp + \
                      self.game_text[self.cwPtr + len(tmp):]
                self.sampleTxt.setText(tmp)
                self.cwPtr += len(self.splitted[self.correct_words]) + 1
                self.correct_words += 1

                prcnt = int((self.correct_words / float(len(self.splitted))) * 100)
                send_progress.apply_async([NAME, self.game_name, prcnt])

                # self.pbar.setValue(get_progres(NAME))
                # self.plbl.setText(str(get_progres(NAME)) + "%")
                # self.plbl.adjustSize()

                self.timer.start(100)

            self.lbl.setText(str(self.correct_words))
            self.lbl.adjustSize()

            if self.correct_words == len(self.splitted):
                self.lbl.setText("Finish")
                self.lbl.adjustSize()
                # self.end_time = time.perf_counter()s

                # pace = 60 * ((self.stxtLen - self.stxtSpace) / (
                #         self.end_time - self.start_time))
                # pace = str(round(pace, 2))
                # TODO: 
                # self.pacelbl.setText(pace + " sym/min") 
                # self.pacelbl.adjustSize()


    def restartBtn(self):
        print("restart")
        self.reset()



if __name__ == '__main__':
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

        QLabel#sample_text{
            padding: 5px;
            font-size: 18px;
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

        QProgressBar {
            border: 2px solid #242424;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #242424;
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
    """
    App.setStyleSheet(style)

    window = TrainingWin()
    App.exec()
