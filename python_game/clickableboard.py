import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Score import Score
from Piece import Piece
import time
import re

MAT_DIM = 20
IMG_BOMB = "./images/bomb.png"

STATUS_READY = 0
STATUS_PLAYING = 1

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        hbox = QHBoxLayout()

        self.score = Score()

        self.clock = QLabel()
        self.clock.setFixedSize(100, 100)
        self.clock.setText("030")
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.clock.setFont(QFont('Times', 14))
        self.clock.setStyleSheet("border : 2px solid black;"
                                 "background : lightgrey;")

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        # Gridul cu bombe
        self.win = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.win.setStyleSheet("background-color:black;")

        self.scoreBoard = QLabel()
        self.scoreBoard.setText("Get the highest score in 30 seconds! ")
        self.scoreBoard.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.scoreBoard.setFont(QFont('Times', 14))
        self.scoreBoard.setStyleSheet("border : 2px solid black;"
                                      "background : lightgrey;")

        hbox.setAlignment(Qt.AlignTop)
        hbox.addWidget(self.scoreBoard)
        hbox.addWidget(self.clock)
        hbox.addWidget(self.score)

        vertical = QVBoxLayout(self)
        vertical.addLayout(hbox)
        vertical.addWidget(self.win)

        self.setLayout(vertical)
        self.setGeometry(400, 400, 450, 400)

        self.initMap()

        self.update_status(STATUS_READY)

        self.win.setGeometry(100, 100, 200, 200)
        self.win.setLayout(self.grid)
        self.win.setWindowTitle("Bomb destroyer!")

        self.show()

    def update_status(self, status):
        self.status = status

    def initMap(self):
        for i in range(0, MAT_DIM):
            for j in range(0, MAT_DIM):
                piece = Piece(i, j, random.randint(0, 5))
                self.grid.addWidget(piece, i, j)
                piece.clicked.connect(self.triggerStart)
                piece.expandable.connect(self.triggerExpand)

    def resetMap(self):
        for i in range(0, MAT_DIM):
            for j in range(0, MAT_DIM):
                self.grid.itemAtPosition(i, j).widget().close()
                self.grid.itemAtPosition(i, j).widget().deleteLater()

    def update_timer(self):
        if self.status == STATUS_PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)
            if n_secs == 30:
                last_score = int(re.search(r'\d+', self.scoreBoard.text()).group())
                if (int(self.score.value > int(last_score))):
                    self.scoreBoard.setText("Try to beat this: " + str(self.score.value))

                print(self.score.value)
                self.resetGame()
                self.update_status(STATUS_READY)

    def resetGame(self):
        self.clock.setText("030")
        self.resetMap()
        self.initMap()
        self.score.value = 0
        self.score.combo = 1
        self.score.score.setText("Score: " + str(self.score.value))

    def triggerStart(self):
        if self.status != STATUS_PLAYING:
            # First click.
            self.update_status(STATUS_PLAYING)
            self._timer_start_nsecs = int(time.time())

    def generateAndFillOnTop(self, x, y):
        piece = Piece(x, y, random.randint(0, 5))
        self.grid.addWidget(piece, x, y)
        piece.clicked.connect(self.triggerStart)
        piece.expandable.connect(self.triggerExpand)

        piece = Piece(x - 1, y, random.randint(0, 5))
        self.grid.addWidget(piece, x - 1, y)
        piece.clicked.connect(self.triggerStart)
        piece.expandable.connect(self.triggerExpand)

        piece = Piece(x, y, random.randint(0, 5))
        self.grid.addWidget(piece, x - 2, y)
        piece.clicked.connect(self.triggerStart)
        piece.expandable.connect(self.triggerExpand)

    def destroyAndFillHorizotally(self, x, y):
        piece = self.grid.itemAtPosition(x, y).widget()
        fpiece = self.grid.itemAtPosition(x, y + 1).widget()
        spiece = self.grid.itemAtPosition(x, y + 2).widget()

        if (piece.text() == fpiece.text() == spiece.text()):

            while x > 0:
                piece.close()
                fpiece.close()
                spiece.close()
                piece.deleteLater()
                fpiece.deleteLater()
                spiece.deleteLater()

                col = self.grid.itemAtPosition(x - 1, y).widget().text()
                new_piece = Piece(x, y, int(col))
                piece.close()
                piece.deleteLater()
                self.grid.addWidget(new_piece, x, y)
                new_piece.clicked.connect(self.triggerStart)
                new_piece.expandable.connect(self.triggerExpand)

                col = self.grid.itemAtPosition(x - 1, y + 1).widget().text()
                new_piece = Piece(x, y + 1, int(col))
                fpiece.close()
                fpiece.deleteLater()
                self.grid.addWidget(new_piece, x, y + 1)
                new_piece.clicked.connect(self.triggerStart)
                new_piece.expandable.connect(self.triggerExpand)

                col = self.grid.itemAtPosition(x - 1, y + 2).widget().text()
                new_piece = Piece(x, y + 2, int(col))
                spiece.close()
                spiece.deleteLater()
                self.grid.addWidget(new_piece, x, y + 2)
                new_piece.clicked.connect(self.triggerStart)
                new_piece.expandable.connect(self.triggerExpand)

                x = x - 1

                piece = self.grid.itemAtPosition(x, y).widget()
                fpiece = self.grid.itemAtPosition(x, y + 1).widget()
                spiece = self.grid.itemAtPosition(x, y + 2).widget()

            piece.close()
            fpiece.close()
            spiece.close()

            piece.deleteLater()
            fpiece.deleteLater()
            spiece.deleteLater()

            piece = Piece(0, y, random.randint(0, 5))
            self.grid.addWidget(piece, 0, y)
            piece.clicked.connect(self.triggerStart)
            piece.expandable.connect(self.triggerExpand)

            fpiece = Piece(0, y + 1, random.randint(0, 5))
            self.grid.addWidget(fpiece, 0, y + 1)
            fpiece.clicked.connect(self.triggerStart)
            fpiece.expandable.connect(self.triggerExpand)

            spiece = Piece(0, y + 2, random.randint(0, 5))
            self.grid.addWidget(spiece, 0, y + 2)
            spiece.clicked.connect(self.triggerStart)
            spiece.expandable.connect(self.triggerExpand)

            return 1

        return 0

    def destroyAndFillVertical(self, x, y):

        piece = self.grid.itemAtPosition(x, y).widget()
        fpiece = self.grid.itemAtPosition(x - 1, y).widget()
        spiece = self.grid.itemAtPosition(x - 2, y).widget()

        if (piece.text() == fpiece.text() == spiece.text()):
            try:
                while x > 0:

                    piece.close()
                    fpiece.close()
                    spiece.close()

                    piece.deleteLater()
                    fpiece.deleteLater()
                    spiece.deleteLater()

                    if (x <= 2):
                        self.generateAndFillOnTop(x, y)

                        return 1

                    col = self.grid.itemAtPosition(x - 3, y).widget().text()
                    new_piece = Piece(x, y, int(col))
                    piece.close()
                    piece.deleteLater()
                    self.grid.addWidget(new_piece, x, y)
                    new_piece.clicked.connect(self.triggerStart)
                    new_piece.expandable.connect(self.triggerExpand)
                    x = x - 1

                    if (x <= 2):
                        self.generateAndFillOnTop(x, y)
                        return 1

                    col = self.grid.itemAtPosition(x - 3, y).widget().text()
                    new_piece = Piece(x, y, int(col))
                    fpiece.close()
                    fpiece.deleteLater()
                    self.grid.addWidget(new_piece, x, y)
                    new_piece.clicked.connect(self.triggerStart)
                    new_piece.expandable.connect(self.triggerExpand)
                    x = x - 1

                    if (x <= 2):
                        self.generateAndFillOnTop(x, y)
                        return 1

                    col = self.grid.itemAtPosition(x - 3, y).widget().text()
                    new_piece = Piece(x, y, int(col))
                    spiece.close()
                    spiece.deleteLater()
                    self.grid.addWidget(new_piece, x, y)
                    new_piece.clicked.connect(self.triggerStart)
                    new_piece.expandable.connect(self.triggerExpand)
                    x = x - 1

                    piece = self.grid.itemAtPosition(x, y).widget()
                    fpiece = self.grid.itemAtPosition(x - 1, y).widget()
                    spiece = self.grid.itemAtPosition(x - 2, y).widget()




            except:
                pass

        return 0

    def destroyAndGenerate(self, x1, y1, x2, y2, x, y):
        piece = self.grid.itemAtPosition(x, y).widget()
        fpiece = self.grid.itemAtPosition(x1, y1).widget()
        spiece = self.grid.itemAtPosition(x2, y2).widget()

        if (piece.text() == fpiece.text() == spiece.text()):
            piece.deleteLater()
            piece = Piece(x, y, random.randint(0, 5))
            self.grid.addWidget(piece, x, y)
            piece.clicked.connect(self.triggerStart)
            piece.expandable.connect(self.triggerExpand)
            fpiece.deleteLater()
            fpiece = Piece(x1, y1, random.randint(0, 5))
            self.grid.addWidget(fpiece, x1, y1)
            fpiece.clicked.connect(self.triggerStart)
            fpiece.expandable.connect(self.triggerExpand)
            spiece.deleteLater()
            spiece = Piece(x2, y2, random.randint(0, 5))
            self.grid.addWidget(spiece, x2, y2)
            spiece.clicked.connect(self.triggerStart)
            spiece.expandable.connect(self.triggerExpand)
            return 1

        return 0

    def swapBomb(self, x, y, x1, y1, piece, pieceToSwap):
        col = int(piece.text())
        colToSwap = int(pieceToSwap.text())

        piece.close()
        pieceToSwap.close()
        piece.deleteLater()
        pieceToSwap.deleteLater()

        piece = Piece(x1, y1, col)
        pieceToSwap = Piece(x, y, colToSwap)

        self.grid.addWidget(piece, x1, y1)
        self.grid.addWidget(pieceToSwap, x, y)

        piece.clicked.connect(self.triggerStart)
        piece.expandable.connect(self.triggerExpand)

        pieceToSwap.clicked.connect(self.triggerStart)
        pieceToSwap.expandable.connect(self.triggerExpand)

    def swapBombs(self, x, y):
        piece = self.grid.itemAtPosition(x, y).widget()
        ok = 0

        if x > 0:
            pieceToSwap = self.grid.itemAtPosition(x - 1, y).widget()

            if piece.text() != pieceToSwap.text():
                self.swapBomb(x, y, x - 1, y, piece, pieceToSwap)
                ok = 1

        if y < MAT_DIM and ok == 0:
            pieceToSwap = self.grid.itemAtPosition(x, y + 1).widget()

            if piece.text() != pieceToSwap.text():
                self.swapBomb(x, y, x, y + 1, piece, pieceToSwap)
                ok = 1

        if x < MAT_DIM and ok == 0:
            pieceToSwap = self.grid.itemAtPosition(x + 1, y).widget()

            if piece.text() != pieceToSwap.text():
                self.swapBomb(x, y, x + 1, y, piece, pieceToSwap)
                ok = 1

        if y > 0 and ok == 0:
            pieceToSwap = self.grid.itemAtPosition(x, y - 1).widget()

            if piece.text() != pieceToSwap.text():
                self.swapBomb(x, y, x, y - 1, piece, pieceToSwap)
                ok = 1

        return ok

    def triggerExpand(self, x, y):

        try:
            if x - 2 >= 0:
                ok = self.destroyAndFillVertical(x, y)

                if ok:
                    print(ok)
                    print("distrugem vertical de jos in sus")
                    self.score.incrScore()



                else:
                    print("nu se mai poate de jos in sus")

                    if y + 2 < MAT_DIM:
                        ok = self.destroyAndFillHorizotally(x, y)

                        if ok:
                            print(ok)
                            print("distrugen orizontal de la stanga la dreapta")
                            self.score.incrScore()


                        else:
                            print("nu se mai poate de la stanga la dreapta")

                            if x + 2 < MAT_DIM:
                                ok = self.destroyAndFillVertical(x + 2, y)

                                if ok:
                                    print(ok)
                                    self.score.incrScore()

                                    print("distrugem vertical 3 sus in jos")

                                else:
                                    print("nu se mai poate de sus in jos")

                                    if y - 2 > 0:
                                        ok = self.destroyAndFillHorizotally(x, y - 2)

                                        if ok:
                                            print(ok)
                                            self.score.incrScore()

                                            print("distrugen orizontal de la dreapta la dreapta")
                                        else:
                                            print("nu se mai poate de la dreapta la stanga")







            else:
                ok = self.destroyAndFillHorizotally(x, y)
                print(ok)
                if ok == 1:
                    self.score.incrScore()

            self.swapBombs(x, y)
            self.score.combo = 1

        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
