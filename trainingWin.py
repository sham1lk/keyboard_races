import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import random


class TrainingWin(QWidget):
	# constructor
	def __init__(self):
		super().__init__()
		self.sample_text = []
		self.sample_text.append("In some natures there are no half-tones;\nnothing but raw primary colours. John Bodman\nwas a man who was always at one extreme or the other")
		self.sample_text.append("When and where, it matters not now to\nrelate--but once upon a time as I was\npassing through a thinly peopled district\nof country, night came down upon me, almost unawares.")
		self.sample_text.append("Some women had risen, in order to get\nnearer to him, and were standing with their\neyes fastened on the clean-shaven face\nof the judge, who was saying such weighty things")
		self.sample_text.append("Conradin hated her with a desperate sincerity\nwhich he was perfectly able to mask.")
		self.sample_text.append("The man held a double-barrelled gun cocked in his\nhand, and screwed up his eyes in the direction\nof his lean old dog who was running on ahead sniffing the bushes")
		self.idx = random.randint(0, len(self.sample_text)-1)
		self.stxtLen = len(self.sample_text[self.idx])
		self.stxtSpace = self.sample_text[self.idx].count(' ')
		self.splitted = self.sample_text[self.idx].split()

		self.wgtW = 800
		self.wgtH = 600
		self.setGeometry(100, 100, self.wgtW, self.wgtH)
		self.setWindowTitle("New Game")
		self.training_ui()

		self.correct_words = 0
		self.started = False
		self.start_time = 0.0;
		self.end_time = 0.0;
		self.cwPtr = 0


	def training_ui(self):
		self.sampleTxt = QLabel(self)
		self.sampleTxt.setGeometry(285, 140, 260, 60)
		self.sampleTxt.setFont(QFont('Times', 15))
		self.sampleTxt.setAlignment(Qt.AlignCenter)
		self.sampleTxt.setText(self.sample_text[self.idx])
		self.sampleTxt.adjustSize()
		h1 = int(self.sampleTxt.height() * 1.6)
		w1 = int(self.sampleTxt.width() * 1.3)
		stx = (self.wgtW - w1)/2
		sty = (self.wgtH - h1)/5
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
		pbrx = (self.wgtW-pbrW)/2
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

		if self.correct_words != len(self.splitted):
			if text == (self.splitted[self.correct_words]+" "):
				self.qle.clear()

				tmp = '_'*len(self.splitted[self.correct_words])
				tmp = self.sample_text[self.idx][:self.cwPtr] + tmp + self.sample_text[self.idx][self.cwPtr+len(tmp):]
				self.sampleTxt.setText(tmp)
				self.cwPtr += len(self.splitted[self.correct_words]) + 1
				self.correct_words += 1

				prcnt = int((self.correct_words/float(len(self.splitted))) * 100)
				self.pbar.setValue(prcnt)
				self.plbl.setText(str(prcnt) + "%")
				self.plbl.adjustSize()

			self.lbl.setText(str(self.correct_words))
			self.lbl.adjustSize()

			if self.correct_words == len(self.splitted):
				self.lbl.setText("Congratulations")
				self.lbl.adjustSize()
				self.end_time = time.perf_counter()

				pace = 60 * ((self.stxtLen - self.stxtSpace) / (self.end_time - self.start_time))
				pace = str(round(pace, 2))
				self.pacelbl.setText(pace + " sym/min")
				self.pacelbl.adjustSize()


	# def endTraining(self):
	# 	pass


if __name__ == '__main__':
	App = QApplication(sys.argv)
	window = TrainingWin()
	App.exec()
