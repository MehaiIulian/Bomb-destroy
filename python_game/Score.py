from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Score(QWidget):
    value = 0
    combo = 1

    def __init__(self):
        super().__init__()
        self.score = QLabel("Score : 0", self)
        self.score.setGeometry(50, 0, 100, 50)

        # setting alignment
        self.score.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # setting font
        self.score.setFont(QFont('Times', 14))
        self.score.setStyleSheet("QLabel"
                                 "{"
                                 "border : 2px solid black;"
                                 "color : green;"
                                 "background : lightgrey;"
                                 "}")

    def incrScore(self):
        self.value = self.value + self.combo * 10
        self.combo += 1
        self.score.setText("Score : " + str(self.value))
