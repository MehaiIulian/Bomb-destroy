import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Score import Score
import numpy as np
import time
import re

MAT_DIM = 20
IMG_BOMB = "./images/bomb.png"

STATUS_READY = 0
STATUS_PLAYING = 1

class Piece(QPushButton):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()

    def __init__(self, x, y, COL, *args, **kwargs):
        super(Piece, self).__init__(*args, **kwargs)

        self.setMinimumSize(QSize(30, 30))
        self.setMaximumSize(QSize(100, 100))

        self.x = x
        self.y = y
        self.color = COL

        self.setText(str(self.color))

        self.setIcon(QIcon(IMG_BOMB))

        self.vect = ["rgba(255, 1, 1, 1)", "rgba(1,255, 1, 1)", "rgba(1,1,255,1)", "rgba(1,255,255,1)",
                     "rgba(255,1,247,1)", "rgba(100,100,100,1)"]
        if self.color == 0:
            self.setStyleSheet(f"color :{self.vect[0]};"
                               f"background-color: {self.vect[0]};")
        elif self.color == 1:
            self.setStyleSheet(f"color :{self.vect[1]}; background-color: {self.vect[1]}")

        elif self.color == 2:
            self.setStyleSheet(f"color :{self.vect[2]}; background-color: {self.vect[2]}")

        elif self.color == 3:
            self.setStyleSheet(f"color :{self.vect[3]}; background-color: {self.vect[3]}")

        elif self.color == 4:
            self.setStyleSheet(f"color :{self.vect[4]}; background-color: {self.vect[4]}")
        else:
            self.setStyleSheet(f"color :{self.vect[5]}; background-color: {self.vect[5]}")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def __repr__(self):
        return "(Piece at " + str(self.posX) + " and " + str(
            self.posY) + " of color " + str(self.colorPiece) + ")"

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.click()

    def click(self):

        self.expandable.emit(self.x, self.y)
        self.clicked.emit()