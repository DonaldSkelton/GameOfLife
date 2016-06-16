import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep
from threading import Thread


class GameOfLife(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.buttons=[]
        for x in range(50):
            self.buttons.append(list())
            for y in range(50):
                self.buttons[x].append(QPushButton(self))
                self.buttons[x][y].setStyleSheet('background-color: #fff')            
                self.buttons[x][y].setGeometry(x*15+20,y*15+20,15,15)
                self.buttons[x][y].clicked.connect(self.cellClick)
        self.btnPlay=QPushButton('Play',self)
        self.btnPlay.move(195,790)
        self.btnPlay.clicked.connect(self.playClick)
        self.btnPause=QPushButton('Pause',self)
        self.btnPause.move(295,790)
        self.btnPause.clicked.connect(self.pauseClick)
        self.btnClear=QPushButton('Clear',self)
        self.btnClear.move(395,790)
        self.btnClear.clicked.connect(self.clearClick)
        self.btnRand=QPushButton('Random',self)
        self.btnRand.move(495,790)
        self.btnRand.clicked.connect(self.randClick)
        self.setGeometry(100,45,790,845)
        self.show()
        self.setWindowTitle('Conway\'s Game of Life')
        self.paused = True
        self.connect(self, SIGNAL("paintSignal(PyQt_PyObject)"), self.paintGrid)

    def cellClick(self):
        if not self.paused:
            self.pauseClick()
        if self.sender().styleSheet() == 'background-color: #000' :
            self.sender().setStyleSheet('background-color: #fff')
        else:
            self.sender().setStyleSheet('background-color: #000')
    
    def pauseClick(self):
        self.paused = True
        sleep(0.3)
        self.btnPlay.setEnabled(True)        

    def paintGrid(self, grid):
        for n in range(2500):
            x = n // 50            
            y = n % 50
            if grid[n]==0:
                self.buttons[x][y].setStyleSheet('background-color: #fff')
            else:
                self.buttons[x][y].setStyleSheet('background-color: #000')

    def randClick(self):
        if not self.paused:
            self.pauseClick()
        from random import randint
        grid=[randint(0,101) % 2 for _ in range(2500)]
        self.paintGrid(grid)
    
    def clearClick(self):
        if not self.paused:
            self.pauseClick()
        grid=[0 for _ in range(2500)]
        self.paintGrid(grid)
    
    def countNeighbors(self, col, row, grid):
        rows = range(max(0, row-1), min(row+2, len(grid)))
        cols = range(max(0, col-1), min(col+2, len(grid[0])))
        return sum(grid[c][r] for r in rows for c in cols) - grid[col][row]
    
    def playClick(self):
        if not self.paused:
            return
        else:
            self.paused = False
            self.btnPlay.setEnabled(False)
        def lifeCycle(self):
            while not self.paused:
                current=[[1 if cell.styleSheet() == 'background-color: #000' else 0 for cell in cols] for cols in self.buttons]
                grid=[]
                ncount=0
                for x in range(50):
                    for y in range(50):
                        ncount=self.countNeighbors(x,y,current)
                        if ncount < 2 or ncount > 3:
                            grid.append(0)
                        elif current[x][y] == 1:
                            grid.append(1)
                        elif ncount == 3:
                            grid.append(1)
                        else:
                            grid.append(0)
                self.emit(SIGNAL("paintSignal(PyQt_PyObject)"), grid)
                sleep(0.25)
        t=Thread(target=lifeCycle, args=(self, ))
        t.start()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=GameOfLife()
    sys.exit(app.exec_())
