import numpy as np

class DummySim:
    def __init__(self, field_size: (int, int), n_bots: int, p_resource: float):
        self.field_size_x = field_size[0]
        self.field_size_y = field_size[1]
        self.n_bots = n_bots
        self.p_resource = p_resource
        self.bot_coordinates = dict()

    def init_resources(self):
        chances_field = np.random.rand(self.field_size_x, self.field_size_y)
        self.resource_field = np.zeros((self.field_size_x, self.field_size_y))
        self.resource_field[chances_field < self.p_resource] = 1 

    def init_bots(self):
        center_x = self.field_size_x // 2
        center_y = self.field_size_y // 2

def main():
    my_sim = DummySim(field_size = (100, 100), n_bots = 10, p_resource = 0.03)
    my_sim.init_resources()
    print(my_sim.resource_field)
    print(np.sum(my_sim.resource_field))

if __name__ == '__main__':
    main()