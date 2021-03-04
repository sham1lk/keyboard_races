import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import random

# create a Window class
from helpers import get_ip, get_name
sample_text = []
sample_text.append("In some natures there are no half-tones;\n nothing but raw primary colours. John Bodman\n was a man who was always at one extreme or the other")
sample_text.append("When and where, it matters not now to\n relate--but once upon a time as I was\n passing through a thinly peopled district\n of country, night came down upon me, almost unawares.")
sample_text.append("Some women had risen, in order to get\n nearer to him, and were standing with their\n eyes fastened on the clean-shaven face\n of the judge, who was saying such weighty things")
sample_text.append("Conradin hated her with a desperate sincerity\n which he was perfectly able to mask.")
sample_text.append("The man held a double-barrelled gun cocked in his\n hand, and screwed up his eyes in the direction\n of his lean old dog who was running on ahead sniffing the bushes")
idx = random.randint(0, len(sample_text)-1)
splitted = sample_text[idx].split()
wgtW = 800
wgtH = 600

class TrainingWin(QWidget):
	# constructor
	def __init__(self):
		super().__init__()
		self.setGeometry(100, 100, wgtW, wgtH)
		self.setWindowTitle("New Game")
		self.training_ui()

		self.correct_words = 0
		self.started = False
		self.start_time = 0.0;
		self.end_time = 0.0;


	def training_ui(self):
		self.sampleTxt = QLabel(self)
		self.sampleTxt.setGeometry(285, 140, 260, 60)
		self.sampleTxt.setFont(QFont('Times', 15))
		self.sampleTxt.setAlignment(Qt.AlignCenter)
		self.sampleTxt.setText(sample_text[idx])
		self.sampleTxt.adjustSize()
		h1 = int(self.sampleTxt.height() * 1.6)
		w1 = int(self.sampleTxt.width() * 1.3)
		stx = (wgtW - w1)/2
		sty = (wgtH - h1)/5
		self.sampleTxt.setGeometry(stx, sty, w1, h1)
		self.sampleTxt.setStyleSheet("QLabel"
									"{"
									"color : black;"
									"border : 3px solid black;"
									"background : white;"
									"}")

		qlw = 140
		qlh = 25
		w2 = int(stx+(w1-qlw)/2)

		self.qle = QLineEdit(self)
		self.qle.setGeometry(w2, sty+h1+25, qlw, qlh)
		self.qle.textChanged[str].connect(self.onChanged)

		lbly = sty+h1+25
		self.lbl = QLabel(self)
		self.lbl.setText("0")
		self.lbl.setGeometry(w2+qlw+20, lbly, 30, qlh)

		pbrW = 500
		pbrx = (wgtW-pbrW)/2
		pbry = lbly + 120
		self.pbar = QProgressBar(self) 
		self.pbar.setGeometry(pbrx, pbry, pbrW, qlh)

		plby = pbry - 15
		self.plbl = QLabel(self)
		self.plbl.setGeometry(pbrx+5, plby, 30, qlh)
		self.plbl.setText("0%")

		self.pacelbl = QLabel(self)
		self.pacelbl.setGeometry(pbrx+pbrW-100, plby, 50, qlh)

		self.show()


	def onChanged(self, text):
		if not self.started:
			self.start_time = time.perf_counter()
			self.started = True

		if self.correct_words != len(splitted):
			if text == (splitted[self.correct_words]+" "):
				self.correct_words += 1
				self.qle.clear()

				prcnt = int((self.correct_words/float(len(splitted))) * 100)
				self.pbar.setValue(prcnt)
				self.plbl.setText(str(prcnt) + "%")
				self.plbl.adjustSize()

			self.lbl.setText(str(self.correct_words))
			self.lbl.adjustSize()

			if self.correct_words == len(splitted):
				self.lbl.setText("Congratulations")
				self.lbl.adjustSize()
				self.end_time = time.perf_counter()

				pace = 60 * ((len(sample_text[idx]) - sample_text[idx].count(' ')) / (self.end_time - self.start_time))
				pace = str(round(pace, 2))
				self.pacelbl.setText(pace + " sym/min")
				self.pacelbl.adjustSize()


	# def endTraining(self):
	# 	pass



# create pyqt5 app
App = QApplication(sys.argv)


def start_training():
	# create the instance of our Window
	window = TrainingWin()
	App.exec()
	# start the app
	# sys.exit(App.exec())

start_training()


