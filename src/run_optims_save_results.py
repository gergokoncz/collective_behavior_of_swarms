#!/usr/bin/env python3

import numpy as np
import pyswarms as ps

from pathlib import Path

from geneal.genetic_algorithms import ContinuousGenAlgSolver

from simulation.BaseSimulation import *
from simulation.PSimulation import *



class Logline:
    def __init__(self):
        self.optim_alg: str = ""
        self.run: str = ""

        self.pso_steps: str = ""
        self.pso_n_particles: str = ""
        self.pso_iters: str = ""

        self.gen_pop_size: str = ""
        self.gen_mutation_rate: str = ""
        self.gen_selection_rate: str = ""
        self.gen_selection_strategy: str = ""

        self.field_x: str = ""
        self.field_y: str = ""
        self.n_bots: str = ""
        self.trail_decay: str = ""
        self.p_resource: str = ""
        self.resource_dist_mean: str = ""
        self.resource_dist_std: str = ""

        self.p_leave: str = ""
        self.p_follow: str = ""
        self.cost: str = ""
        self.is_selected: str = ""

        self.file_path = Path.cwd().parent.joinpath('results').joinpath('all_results.csv')
        self.file = open(file_path, 'a')

    def write_log_line(self):
        pass



def genal_fitness(p):

    return lambda chromosome: genal_call_psim(chromosome, p)


def genal_call_psim(x, p, steps = 500):
    my_sim = ProbabilisticSimulation(
        field_size = (100, 100), 
        n_bots=10,
        p_resource = p,
        resource_dist = (10, 3),
        p_leave_trail = x[0],
        p_follow_trail = x[1]
        )
    my_sim.init_resources()
    my_sim.init_bots()
    for _ in range(steps):
        my_sim.simulate_step()

    #print(my_sim.stored_food)
    return my_sim.stored_food


def genal_optim(p):
    solver = ContinuousGenAlgSolver(
        n_genes = 2,
        fitness_function = genal_fitness(p),
        pop_size = 10,
        mutation_rate = 0.1,
        selection_rate = 0.6,
        selection_strategy = "roulette_wheel",
        problem_type = float,
        variables_limits = (0, 1),
        verbose = True,
        show_stats = True,
        plot_results = True
    )
    solver.solve()
    print("solved")
    print(solver)
    print(type(solver))


def call_psim(x, p, steps = 10_000):
    print(type(x))
    print(p)
    result = np.zeros(x.shape[0])

    for i in range(x.shape[0]):
        my_sim = ProbabilisticSimulation(
            field_size = (100, 100), 
            n_bots=10,
            p_resource = p,
            resource_dist = (10, 3),
            p_leave_trail = x[i][0],
            p_follow_trail = x[i][1]
            )
        my_sim.init_resources()
        my_sim.init_bots()
        for _ in range(steps):
            my_sim.simulate_step()

        result[i] = -my_sim.stored_food
    print(x)
    print(np.mean(x, axis = 0))
    print(result)
    print(np.mean(result))

    return result


def pso_optim(p, steps = 5_000) -> None:
    options = {'c1': 0.5, 'c2': 0.5, 'w': 0.05}
    bounds = (np.zeros(2), np.ones(2))
    optimizer = ps.single.GlobalBestPSO(n_particles = 10, dimensions = 2, options = options, bounds = bounds)
    s = optimizer.optimize(call_psim, iters = 20, p = p, steps = steps)
    return s



def main() -> None:
    s = pso_optim(p = 0.01, steps = 5_000)

    

    #genal_optim(0.01)

if __name__ == '__main__':
    main()
