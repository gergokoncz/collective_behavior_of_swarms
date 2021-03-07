import numpy as np
from random import random
from typing import Tuple

from simulation.BaseSimulation import *


class ProbabilisticBot(BaseBot):
    
    def __init__(self, pos_x: int, pos_y: int, *, p_leave_trail: float, p_follow_trail: float):
        super().__init__(pos_x, pos_y)

        self.p_leave_trail: float = p_leave_trail
        self.p_follow_trail: float = p_follow_trail

        self.leave_mark: bool = False

    def step(self) -> Tuple[int, int, bool]:
        """
        Overwrite of parent class func
        returns also whether bot leaves pheromone mark
        """
        return *super().step(), self.leave_mark

    def pick_up_food(self) -> None:
        """
        Overwrite of parent class func
        Has to make decision whether to leave mark or not
        """
        super().pick_up_food()
        if random.random() < self.p_leave_trail:
            self.leave_mark = True

    def store_food(self) -> None:
        """
        Overwrite of parent class func
        Set mark leaving to False
        """
        super().store_food()
        self.leave_mark = False


class ProbabilisticSimulation(DummySim):
    
    def __init__(self, field_size: Tuple[int, int], n_bots: int, p_resource: float, 
        *, p_leave_trail: float, p_follow_trail: float):
        
        super().__init__(field_size, n_bots, p_resource)

        self.p_leave_trail = p_leave_trail
        self.p_follow_trail = p_follow_trail

        self.trails: Dict[Tuple[int, int]: int] = dict()
    
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


    def trail_decay(self):
        """
        Make trails decay over time
        """
        self.trails = {key: value - 1 for (key, value) in self.trails.items() if value > 1}

    def simulate_step(self) -> None:      

        field_state = {
            'field_size': (self.field_size_x, self.field_size_y),
            'bot_coordinates' : self.bot_coordinates,
            'resource_coordinates': self.resource_set,
            'trails': self.trails,
        }
        
        new_bot_coordinates = set()
        new_trails = set()
        for bot in self.bots:
            
            self.stored_food += bot.update_env(field_state)
            x,y, mark_left = bot.step()
            new_bot_coordinates.add((x, y))
            if mark_left:
                new_trails.add((x, y))

        self.bot_coordinates = new_bot_coordinates
        self.trail_decay()
        for val in new_trails:
            self.trails[val] = 5


def main():
    my_sim = ProbabilisticSimulation(field_size = (100, 100), n_bots = 10, p_resource = 0.01, p_leave_trail = 1, p_follow_trail = 0.5)
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