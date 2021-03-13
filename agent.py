from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

# SIR model with random stepping? Initialisation??

class SIRAgent(Agent):

    def __init__(self, id, model, status=0):

        super().__init__(id, model)

        # 0 is susceptible, 1 infected, 2 recovered, (3 dead)
        self.id = id
        self.status = status
        self.time_since = 0

    def move(self):

        step_options = self.model.grid.get_neighborhood(self.pos,
                                                        moore=True,
                                                        include_center=False)

        new_pos = self.random.choice(step_options)
        self.model.grid.move_agent(self, new_pos)

    def infection(self):

        self.time_since = 0
        self.status = 1

    def step(self):

        self.move()

        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        infection_prob = self.model.infection_prob

        for c in cellmates:

            if (random.uniform(0,1) <= infection_prob) and (c.status == 0) and (self.status==1):

                c.infection()

        if self.status == 1:

            self.time_since += 1

        if self.time_since >= self.model.infection_period:

            if random.uniform(0,1) > .5:
                self.status = 2
            else:
                self.status = 0





