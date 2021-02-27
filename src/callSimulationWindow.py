#!/user/bin/env python3

import sys
import time
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen
from simulation.simulation import *
from gui.SimulationWindow import *

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        
        self.my_sim = DummySim(field_size = (100, 100), n_bots=10, p_resource=0.03)
        self.my_sim.init_resources()
        self.my_sim.init_bots()

        self.frame_x = 100
        self.frame_y = 150
        
        self.ui = Ui_ForagingAntsSimulation()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.startAnimation)
        self.show()

    def startAnimation(self):
        for _ in range(100):
            self.my_sim.simulate_step()
            time.sleep(0.5)
            print(self.my_sim.bot_coordinates)
            self.drawAgain()

    def drawAgain(self):
        self.update()

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        
        # draw frames
        pen = QPen(Qt.black, 2)
        qp.setPen(pen)
        qp.drawLine(self.frame_x, self.frame_y, self.frame_x + 500, self.frame_y)
        qp.drawLine(self.frame_x, self.frame_y + 500, self.frame_x + 500, self.frame_y + 500)
        qp.drawLine(self.frame_x, self.frame_y, self.frame_x, self.frame_y + 500)
        qp.drawLine(self.frame_x + 500, self.frame_y, self.frame_x + 500, self.frame_y + 500)

        # draw bots
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        
        for bot in self.my_sim.bot_coordinates:
            qp.drawEllipse(self.frame_x + bot[0] * 5, self.frame_y + bot[1] * 5, 5, 5)
        
        # draw resources
        qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        for resource in self.my_sim.resource_set:
            qp.drawRect(self.frame_x + resource[0] * 5, self.frame_y + resource[1] * 5, 3, 3)

        qp.end()



def main():
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()