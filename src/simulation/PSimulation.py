import numpy as np
from typing import Tuple

from BaseSimulation import *


class ProbabilisticBot(BaseBot):
    
    def __init__(self, pos_x, pos_y, *, p_leave_trail, p_follow_trail):
        super().__init__(pos_x, pos_y)

        self.p_leave_trail = p_leave_trail
        self.p_follow_trail = p_follow_trail

class ProbabilisticSimulation(DummySim):
    
    def __init__(self, field_size: Tuple[int, int], n_bots: int, p_resource: float, 
        *, p_leave_trail: float, p_follow_trail: float):
        
        super().__init__(field_size, n_bots, p_resource)

        self.p_leave_trail = p_leave_trail
        self.p_follow_trail = p_follow_trail
    
    def init_bots(self) -> None:
        """
        Initialize bots for sim
        """
        center_x = self.field_size_x // 2
        center_y = self.field_size_y // 2
        
        for _ in range(self.n_bots):
            rand_vals = np.random.randint(- self.field_size_x // 5, self.field_size_y // 5 + 1, 2)
            x, y = center_x + rand_vals[0], center_y + rand_vals[1]
            
            while (x, y) in self.bot_coordinates:
                rand_vals = np.random.randint(- self.field_size_x // 5, self.field_size_y // 5 + 1, 2)
                x, y = center_x + rand_vals[0], center_y + rand_vals[1]
            
            self.bot_coordinates.add((x, y))
            self.bots.append(ProbabilisticBot(x, y, p_leave_trail = self.p_leave_trail, p_follow_trail = self.p_follow_trail))


def main():
    my_sim = ProbabilisticSimulation(field_size = (100, 100), n_bots = 10, p_resource = 0.01, p_leave_trail = 0.5, p_follow_trail = 0.5)
    my_sim.init_resources()
    my_sim.init_bots()
    for _ in range(1000):
        if _ % 1000 == 99:
            print(f'\nRound {_}\n')
            print(f'{my_sim.bot_coordinates}')
        my_sim.simulate_step()

    print(f'{my_sim.stored_food}')
    None

if __name__ == '__main__':
    main()