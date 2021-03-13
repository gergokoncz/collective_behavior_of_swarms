#!/usr/bin/env python3

import random

import numpy as np
from pathlib import Path
from typing import Tuple

if 'simulation' in str(Path().cwd()):
    from BaseSimulation import *
else:
    from simulation.BaseSimulation import *


class ProbabilisticBot(BaseBot):
    
    def __init__(self, pos_x: int, pos_y: int, *, p_leave_trail: float, p_follow_trail: float):
        super().__init__(pos_x, pos_y)

        self.p_leave_trail: float = p_leave_trail
        self.p_follow_trail: float = p_follow_trail

        self.leave_mark: bool = False
        self.tracking_on: bool = False

    
    def pick_up_food(self) -> None:
        """
        Overwrite of parent class func
        Has to make decision whether to leave mark or not
        """
        super().pick_up_food()
        if random.random() < self.p_leave_trail:
            self.leave_mark = True

        self.tracking_on = False

    
    def store_food(self) -> None:
        """
        Overwrite of parent class func
        Set mark leaving to False
        """
        super().store_food()
        self.leave_mark = False

    
    def is_on_trail(self) -> bool:
        """
        Return if bot is on trail
        """
        return (self.pos_x, self.pos_y) in self.current_field_state['trails']

    
    def check_for_trail(self) -> None:
        """
        Check for pheromone trail in proximity
        """
        if (self.pos_x - 1, self.pos_y) in self.current_field_state['trails']:
            self.trails_sensed.add('u')

        if (self.pos_x + 1, self.pos_y) in self.current_field_state['trails']:
            self.trails_sensed.add('d')

        if (self.pos_x, self.pos_y + 1) in self.current_field_state['trails']:
            self.trails_sensed.add('r')

        if (self.pos_x, self.pos_y - 1) in self.current_field_state['trails']:
            self.trails_sensed.add('l')

        # only keep directions to food and not to center
        for el in self.get_dir_to_storage_unit():
            self.trails_sensed.discard(el) 

    
    def decide_to_track(self) -> None:
        """
        Make decision whether to track trail or not
        """
        if random.random() < self.p_follow_trail:
            self.tracking_on = True

    
    
    def update_env(self, state: Dict) -> int:

        food_stored = 0

        # set initial state
        self.options = {'u', 'd', 'l', 'r'}
        self.food_dir = set()
        self.trails_sensed = set()

        self.current_field_state = state

        self.storage_x = self.current_field_state['field_size'][0] // 2
        self.storage_y = self.current_field_state['field_size'][1] // 2

        if not self.has_food:
            # if on food grab it and that is what you do for the step
            if self.is_on_food():
                self.pick_up_food()

            else:
                # if not on food check for food in proximity
                self.check_for_close_food() 
                
                if not self.food_one_away:
                    self.check_for_food_two()
                
                # and check for trails
                # 
                if self.tracking_on:
                    self.check_for_trail()
                else:
                    self.check_for_trail()
                    if len(self.trails_sensed) >= 1:
                        self.decide_to_track()
                        if not self.tracking_on:
                            self.trails_sensed = set() 
        else:
            if self.is_in_storage_unit():
                self.store_food()
                food_stored = 1
            
            else:
                self.go_to_storage_unit()

        self.protect_from_collision()
        self.avoid_walls()

        return food_stored
    
    
    def step(self) -> Tuple[int, int, bool]:
        
        if len(self.food_dir) > 0:
            self._move_according_to_direction(random.choice(list(self.food_dir)))
        elif len(self.trails_sensed) > 0:
            self._move_according_to_direction(random.choice(list(self.trails_sensed)))
        elif len(self.options) > 0:
            self._move_according_to_direction(random.choice(list(self.options)))
        # else stay in place
        return self.pos_x, self.pos_y, self.leave_mark


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
    my_sim = ProbabilisticSimulation(field_size = (100, 100), n_bots = 10, p_resource = 0.1, p_leave_trail = 0.2, p_follow_trail = 0.1)
    my_sim.init_resources()
    my_sim.init_bots()
    for _ in range(100000):
        if _ % 100 == 99:
            print(f'\nRound {_}\n')
            print(f'Before step:')
            print(f'bot_coordinates:{my_sim.bot_coordinates}')
            print(f'resource_coordinates:{my_sim.resource_set}')
            for bot in my_sim.bots:
                bot.print_bot()

            my_sim.simulate_step()
            print(f'\nAfter step:')
            print(f'bot_coordinates:{my_sim.bot_coordinates}')
            print(f'resource_coordinates:{my_sim.resource_set}')
            for bot in my_sim.bots:
                bot.print_bot()

    print(f'{my_sim.stored_food}')

if __name__ == '__main__':
    main()