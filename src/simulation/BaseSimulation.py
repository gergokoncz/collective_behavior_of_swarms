#!/usr/bin/env python3

import numpy as np
from typing import Dict, Tuple, List, Set
import random
import math

class BaseBot:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.options: Set = set()
        self.food_dir: Set = set()
        
        self.has_food = False
        self.current_field_state: Dict = dict()

        self.food_one_away = False
        
        self.storage_x: int = -1
        self.storage_y: int = -1

    
    def check_for_close_food(self) -> None:
        """
        Check if food is one away and adjust state accordingly
        """
        
        if (self.pos_x - 1, self.pos_y) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('u')
            self.food_one_away = True
            
            print('food found up')

        if (self.pos_x + 1, self.pos_y) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('d')
            self.food_one_away = True
            
            print('food found down')

        if (self.pos_x, self.pos_y + 1) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('r')
            self.food_one_away = True
            
            print('food found right')

        if (self.pos_x, self.pos_y - 1) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('l')
            self.food_one_away = True
            
            print('food found left')

    
    def check_for_food_two(self) -> None:
        """
        Check if food is two steps away and update state
        """
        if (self.pos_x - 2, self.pos_y) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('u')

        if (self.pos_x + 2, self.pos_y) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('d')
        
        if (self.pos_x, self.pos_y + 2) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('r')
        
        if (self.pos_x, self.pos_y - 2) in self.current_field_state['resource_coordinates']:
            self.food_dir.add('l')
        
        # food two away but get 
        if (self.pos_x - 1, self.pos_y - 1) in self.current_field_state['resource_coordinates']:
            self.food_dir.update({'u', 'l'})
        
        if (self.pos_x - 1, self.pos_y + 1) in self.current_field_state['resource_coordinates']:
            self.food_dir.update({'u', 'r'})
        
        if (self.pos_x + 1, self.pos_y + 1) in self.current_field_state['resource_coordinates']:
            self.food_dir.update({'r', 'd'})
        
        if (self.pos_x + 1, self.pos_y - 1) in self.current_field_state['resource_coordinates']:
            self.food_dir.update({'d', 'l'})

    
    def is_in_storage_proximity(self) -> bool:
        """
        returns whether bot is in storage proximity or not
        """
        return (abs(self.storage_x - self.pos_x) >= 1 and abs(self.storage_y - self.pos_y) >= 1)

    
    def protect_from_collision(self) -> None:
        """
        Check for closeby bots and take out from options
        """
        if not self.has_food and self.is_in_storage_proximity():
            # remove option if collision could happen
            if (self.pos_x - 1, self.pos_y) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('u')
                self.options.discard('u')

            if (self.pos_x + 1, self.pos_y) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('d')
                self.options.discard('d')

            if (self.pos_x, self.pos_y + 1) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('r')
                self.options.discard('r')

            if (self.pos_x, self.pos_y - 1) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('l')
                self.options.discard('l')
        
            # same with two away just to be sure
            if (self.pos_x - 2, self.pos_y) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('u')
                self.options.discard('u')

            if (self.pos_x + 2, self.pos_y) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('d')
                self.options.discard('d')

            if (self.pos_x, self.pos_y + 2) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('r')
                self.options.discard('r')

            if (self.pos_x, self.pos_y - 2) in self.current_field_state['bot_coordinates']:
                self.food_dir.discard('l')
                self.options.discard('l')
        
        # diagonal keep right
        if (self.pos_x - 1, self.pos_y - 1) in self.current_field_state['bot_coordinates']:
            self.food_dir.discard('l')
            self.options.discard('l')

        if (self.pos_x - 1, self.pos_y + 1) in self.current_field_state['bot_coordinates']:
            self.food_dir.discard('u')
            self.options.discard('u')

        if (self.pos_x + 1, self.pos_y + 1) in self.current_field_state['bot_coordinates']:
            self.food_dir.discard('r')
            self.options.discard('r')

        if (self.pos_x + 1, self.pos_y - 1) in self.current_field_state['bot_coordinates']:
            self.food_dir.discard('d')
            self.options.discard('d')

    
    def avoid_walls(self) -> None:
        """
        Can't leave environment
        """
        if self.pos_x == 0:
            print('cant go up')
            self.food_dir.discard('u')
            self.options.discard('u')
        elif self.pos_x >= (self.current_field_state['field_size'][0] - 1):
            print('cant go down')
            self.food_dir.discard('d')
            self.options.discard('d')

        if self.pos_y == 0:
            print('cant go left')
            self.food_dir.discard('l')
            self.options.discard('l')
        elif self.pos_y >= (self.current_field_state['field_size'][1] - 1):
            self.food_dir.discard('r')
            self.options.discard('r')
    
    def go_to_storage_unit(self) -> None:
        """
        Move back to storage unit
        """
        self.options = self.get_dir_to_storage_unit() 
        

    def get_dir_to_storage_unit(self) -> Set['str']:
        """
        Get directions to storage unit
        """
        directions = set()
        
        if self.pos_y > self.storage_y:
            directions.add('l')
        elif self.pos_y < self.storage_y:
            directions.add('r')
        
        if self.pos_x > self.storage_x:
            directions.add('u')
        elif self.pos_x < self.storage_x:
            directions.add('d')

        return directions

    
    def is_on_food(self) -> bool:
        """
        Check if bot stands currently on food
        """
        return (self.pos_x, self.pos_y) in self.current_field_state['resource_coordinates']
    
    
    def is_in_storage_unit(self) -> bool:
        """
        Check if bot stands currently on food
        """
        return self.pos_x == self.storage_x and self.pos_y == self.storage_y

    
    def store_food(self) -> None:
        """
        Drop food and increase storage count
        """
        self.has_food = False
        self.options = set()

    def pick_up_food(self) -> None:
        """
        When on food pick it up
        that is all you do in that round so empties options as well
        """
        self.has_food = True
        self.options = set()
    
    
    def update_env(self, state: Dict) -> int:

        food_stored = 0

        # set initial state
        self.options = {'u', 'd', 'l', 'r'}
        self.food_dir = set()

        self.current_field_state = state

        self.storage_x = self.current_field_state['field_size'][0] // 2
        self.storage_y = self.current_field_state['field_size'][1] // 2

        if not self.has_food:
            # if on food grab it and that is what you do for the step
            if self.is_on_food():
                self.pick_up_food()

            else:
                self.check_for_close_food() 
                
                if not self.food_one_away:
                    self.check_for_food_two()
                
        else:
            if self.is_in_storage_unit():
                self.store_food()
                food_stored = 1
            
            else:
                self.go_to_storage_unit()

        

        self.protect_from_collision()
        self.avoid_walls()

        return food_stored

    
    
    def step(self) -> Tuple[int, int]:
        
        if len(self.food_dir) > 0:
            self._move_according_to_direction(random.choice(list(self.food_dir)))
        elif len(self.options) > 0:
            self._move_according_to_direction(random.choice(list(self.options)))
        # else stay in place
        return (self.pos_x, self.pos_y)
        
    
    def _move_according_to_direction(self, dir: str) -> None:
        """
        Make the move according to chosen direction
        """
        if dir == 'u':
            self.pos_x -= 1
        elif  dir == 'd':
            self.pos_x += 1
        elif dir == 'r':
            self.pos_y += 1
        else:
            self.pos_y -= 1

    
    def print_bot(self) -> None:
        """
        Print bot state
        """
        print(f'x: {self.pos_x}, y : {self.pos_y}')
        print(f'options to go: {self.options}')
        print(f'food seen: {self.food_dir}')

class DummySim:
    def __init__(self, field_size: Tuple[int, int], n_bots: int, p_resource: float):
        
        self.field_size_x = field_size[0]
        self.field_size_y = field_size[1]
        
        self.n_bots = n_bots
        self.bots: List = []
        self.bot_coordinates: Set = set()
        
        self.p_resource = p_resource
        self.resource_set: Set = set()

        self.stored_food = 0


    def init_resources(self) -> None:
        """
        Initialize resources
        """
        chances_field = np.random.rand(self.field_size_x, self.field_size_y)
        self.resource_field = np.zeros((self.field_size_x, self.field_size_y))
        self.resource_field[chances_field < self.p_resource] = 1
        
        xs, ys = np.where(self.resource_field == 1)
        self.resource_set = {(x, y) for x,y in zip(xs, ys)}
        self.resource_set.discard((self.field_size_x // 2, self.field_size_y // 2))

    def init_bots(self) -> None:
        """
        Initialize bots 
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
            self.bots.append(BaseBot(x, y))

    def simulate_step(self) -> None:
        
        field_state = {
            'field_size': (self.field_size_x, self.field_size_y),
            'bot_coordinates' : self.bot_coordinates,
            'resource_coordinates': self.resource_set
        }
        
        new_bot_coordinates = set()
        for bot in self.bots:
            
            self.stored_food += bot.update_env(field_state)
            x,y = bot.step()
            new_bot_coordinates.add((x, y))

        self.bot_coordinates = new_bot_coordinates

    
def main():
    my_sim = DummySim(field_size = (100, 100), n_bots = 10, p_resource = 0.01)
    my_sim.init_resources()
    my_sim.init_bots()
    for _ in range(1000):
        if _ % 1000 == 99:
            print(f'\nRound {_}\n')
            print(f'{my_sim.bot_coordinates}')
        my_sim.simulate_step()

    print(f'{my_sim.stored_food}')

if __name__ == '__main__':
    main()