import numpy as np
from typing import Dict
import random

stored_food = 0

class DummySim:
    def __init__(self, field_size: (int, int), n_bots: int, p_resource: float):
        
        self.field_size_x = field_size[0]
        self.field_size_y = field_size[1]
        
        self.n_bots = n_bots
        self.bots = []
        self.bot_coordinates = set()
        
        self.p_resource = p_resource
        self.resource_set = set()

    def init_resources(self):
        
        chances_field = np.random.rand(self.field_size_x, self.field_size_y)
        self.resource_field = np.zeros((self.field_size_x, self.field_size_y))
        self.resource_field[chances_field < self.p_resource] = 1
        
        xs, ys = np.where(self.resource_field == 1)
        self.resource_set = {(x, y) for x,y in zip(xs, ys)}

    def init_bots(self):
        center_x = self.field_size_x // 2
        center_y = self.field_size_y // 2
        
        for _ in range(self.n_bots):
            rand_vals = np.random.randint(- self.field_size_x // 10, self.field_size_y // 10 + 1, 2)
            x, y = center_x + rand_vals[0], center_y + rand_vals[1]
            
            while (x, y) in self.bot_coordinates:
                rand_vals = np.random.randint(- self.field_size_x // 10, self.field_size_y // 10 + 1, 2)
                x, y = center_x + rand_vals[0], center_y + rand_vals[1]
            
            self.bot_coordinates.add((x, y))
            self.bots.append(Bot(x, y))

    def simulate_step(self):
        
        field_state = {
            'field_size': (self.field_size_x, self.field_size_y),
            'bot_coordinates' : self.bot_coordinates,
            'resource_coordinates': self.resource_set
        }
        
        new_bot_coordinates = set()
        for bot in self.bots:
            
            bot.update_env(field_state)
            x,y = bot.step()
            new_bot_coordinates.add((x, y))

        self.bot_coordinates = new_bot_coordinates

        

class Bot:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.options = []
        self.food_dir = []
        self.has_food = False

    def update_env(self, state: Dict):
        
        self.options = {'u', 'd', 'l', 'r'}
        self.food_dir = set()

        if self.has_food:

            if (self.pos_x, self.pos_y) in state['resource_coordinates']:
                self.has_food = True

            else:
                # food one away, directly there, no questions
                food_one_away = False
                
                if (self.pos_x - 1, self.pos_y) in state['resource_coordinates']:
                    self.food_dir.add('u')
                    print('food found up')
                    food_one_away = True

                if (self.pos_x + 1, self.pos_y) in state['resource_coordinates']:
                    self.food_dir.add('d')
                    print('food found down')
                    food_one_away = True

                if (self.pos_x, self.pos_y + 1) in state['resource_coordinates']:
                    self.food_dir.add('r')
                    print('food found right')
                    food_one_away = True

                if (self.pos_x, self.pos_y - 1) in state['resource_coordinates']:
                    self.food_dir.add('l')
                    food_one_away = True
                
                if not food_one_away:
                    # two away one way for it 
                    if (self.pos_x - 2, self.pos_y) in state['resource_coordinates']:
                        self.food_dir.add('u')

                    if (self.pos_x + 2, self.pos_y) in state['resource_coordinates']:
                        self.food_dir.add('d')
                    
                    if (self.pos_x, self.pos_y + 2) in state['resource_coordinates']:
                        self.food_dir.add('r')
                    
                    if (self.pos_x, self.pos_y - 2) in state['resource_coordinates']:
                        self.food_dir.add('l')
                    
                    # food two away but get 
                    if (self.pos_x - 1, self.pos_y - 1) in state['resource_coordinates']:
                        self.food_dir.update({'u', 'l'})
                    
                    if (self.pos_x - 1, self.pos_y + 1) in state['resource_coordinates']:
                        self.food_dir.update({'u', 'r'})
                    
                    if (self.pos_x + 1, self.pos_y + 1) in state['resource_coordinates']:
                        self.food_dir.update({'r', 'd'})
                    
                    if (self.pos_x + 1, self.pos_y - 1) in state['resource_coordinates']:
                        self.food_dir.update({'d', 'l'})
                
                # remove option if collision could happen
                if (self.pos_x - 1, self.pos_y) in state['bot_coordinates']:
                    self.food_dir.remove('u')
                    self.options.remove('u')

                if (self.pos_x + 1, self.pos_y) in state['bot_coordinates']:
                    self.food_dir.remove('d')
                    self.options.remove('d')

                if (self.pos_x, self.pos_y + 1) in state['bot_coordinates']:
                    self.food_dir.add('r')
                    self.options.add('r')

                if (self.pos_x, self.pos_y - 1) in state['bot_coordinates']:
                    self.food_dir.add('l')
                    self.options.add('l')

        else:
            center_x, center_y = state['field_size']
            center_x //= 2
            center_y //= 2
            # is in center already?
            if self.pos_x == center_x and self.pos_y == center_y:
                global stored_food
                stored_food += 1
                self.has_food = False
                print(stored_food)
            
            else:
                # go to center
                if self.pos_y > center_y:
                    self.options.add('r')
                elif self.pos_y < center_y:
                    self.options.add('l')
                
                if self.pos_x > center_x:
                    self.options.add('u')
                elif self.pos_x < center_x:
                    self.options.add('d')

    def step(self) -> (int, int):
        if len(self.food_dir) > 0:
            self._move_according_to_direction(random.choice(list(self.food_dir)))
        elif len(self.options) > 0:
            self._move_according_to_direction(random.choice(list(self.options)))
        # else stay in place
        return (self.pos_x, self.pos_y)
        
    def _move_according_to_direction(self, dir):
        if dir == 'u':
            self.pos_x -= 1
        elif  dir == 'd':
            self.pos_x += 1
        elif dir == 'r':
            self.pos_y += 1
        else:
            self.pos_y -= 1

    def print_pos(self):
        print(f'x: {self.pos_x}, y : {self.pos_y}')
    

def main():
    my_sim = DummySim(field_size = (100, 100), n_bots = 10, p_resource = 0.1)
    my_sim.init_resources()
    my_sim.init_bots()
    for _ in range(100000):
        my_sim.simulate_step()

if __name__ == '__main__':
    main()