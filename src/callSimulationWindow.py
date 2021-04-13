#!/user/bin/env python3

import sys
import time
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen
from simulation.BaseSimulation import *
from simulation.PSimulation import *
from gui.SimulationWindow import *

# base variables
field_x = 100
field_y = 100

field_constant = 100 / field_x

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        
        self.my_sim = ProbabilisticSimulation(field_size = (field_x, field_y), 
            n_bots=10, p_resource=0.1, resource_dist = (10, 3), p_leave_trail=1, p_follow_trail=1)
        self.my_sim.init_resources()
        self.my_sim.patch_resources()
        self.my_sim.init_bots()

        self.frame_x = 150
        self.frame_y = 150
        
        self.ui = Ui_ForagingAntsSimulation()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.startAnimation)
        self.show()

    def startAnimation(self):
        
        self.my_sim.simulate_step()
        print(self.my_sim.bot_coordinates)
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

        # draw pheromone trails
        if self.my_sim.trails:
            qp.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            for trail in self.my_sim.trails.keys():
                qp.drawEllipse(self.frame_x + trail[1] * 5 * field_constant, 
                    self.frame_y + trail[0] * 5 * field_constant, 2 * field_constant, 2 * field_constant)
        
        # draw storage
        qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        
        for bot in self.my_sim.bot_coordinates:
            qp.drawEllipse(self.frame_x + self.my_sim.field_size_y // 2 * 5 * field_constant, 
                self.frame_y + self.my_sim.field_size_x // 2 * 5 * field_constant, 5 * field_constant, 5 * field_constant)

        # draw resources
        qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        for resource in self.my_sim.resource_dict:
            qp.drawRect(self.frame_x + resource[1] * 5 * field_constant, 
                self.frame_y + resource[0] * 5 * field_constant, 3 * field_constant, 3 * field_constant)
        
        # draw bots
        
        for bot in self.my_sim.bots:
            print(f'\nBot\n')
            bot.print_bot()
            if bot.has_food:
                qp.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            else:
                qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            
            qp.drawEllipse(self.frame_x + bot.pos_y * 5 * field_constant,
                self.frame_y + bot.pos_x * 5 * field_constant, 3 * field_constant, 3 * field_constant)
        

        qp.end()



def main():
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()