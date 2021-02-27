import numpy as np
from typing import Dict

class DummySim:
    def __init__(self, field_size: (int, int), n_bots: int, p_resource: float):
        
        self.field_size_x = field_size[0]
        self.field_size_y = field_size[1]
        
        self.n_bots = n_bots
        self.bots = []
        self.bot_coordinates = []
        
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
            self.bot_coordinates.append([x, y])
            self.bots.append(Bot(x, y))

    def simulate_step(self):
        for bot in self.bots:
            field_state = {
                'field_size': (self.field_size_x, self.field_size_y),
                'bot_coordinates' : self.bot_coordinates,
                'resource_coordinates': self.resource_set
            }
            bot.update_env(field_state)
            bot.step()
        

class Bot:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update_env(self, state: Dict):
        None

    def step():
        None
    

def main():
    my_sim = DummySim(field_size = (100, 100), n_bots = 10, p_resource = 0.05)
    my_sim.init_resources()
    my_sim.init_bots()

if __name__ == '__main__':
    main()