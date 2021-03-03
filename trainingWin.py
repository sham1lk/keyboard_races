import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

# create a Window class
from helpers import get_ip, get_name
sample_text = "Hello motherfucker. Today I am gonna\n teach you a very important lesson.\n But first, let me take a selfie."
splitted = sample_text.split()


class TrainingWin(QWidget):
	# constructor
	def __init__(self):
		super().__init__()
		self.setGeometry(100, 100,800, 600)
		self.setWindowTitle("New Game")
		self.training_ui()

		self.correct_words = 0


	def training_ui(self):
		self.sampleTxt = QLabel(self)
		self.sampleTxt.setGeometry(285, 140, 260, 60)
		self.sampleTxt.setFont(QFont('Times', 15))
		self.sampleTxt.setAlignment(Qt.AlignCenter)
		self.sampleTxt.setText(sample_text)
		self.sampleTxt.adjustSize()
		h1 = int(self.sampleTxt.height() * 1.2)
		w1 = int(self.sampleTxt.width() * 1.1)
		self.sampleTxt.resize(w1, h1)
		self.sampleTxt.setStyleSheet("QLabel"
									"{"
									"color : black;"
									"border : 3px solid black;"
									"background : white;"
									"}")

		w2 = int(285+(w1-140)/2)

		self.lbl = QLabel(self)
		self.lbl.setGeometry(w2+160, 220, 140, 25)
		
		self.qle = QLineEdit(self)
		self.qle.setGeometry(w2, 220, 140, 25)
		self.qle.textChanged[str].connect(self.onChanged)

		self.show()


	def onChanged(self, text):
		if self.correct_words != len(splitted):
			if text == (splitted[self.correct_words]+" "):
				self.correct_words += 1
				self.qle.clear()

			self.lbl.setText(str(self.correct_words))
			self.lbl.adjustSize()

			if self.correct_words == len(splitted):
				self.lbl.setText("Congratulations")
				self.lbl.adjustSize()

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


