from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class SIRAgent(Agent):

    def __init__(self, id, model, immunity_function=lambda x: 1, status=0):

        super().__init__(id, model)

        # 0 is susceptible, 1 infected, 2 recovered, (3 dead)
        self.id = id
        self.status = status
        self.time_since_inf = 0
        self.time_since_recov = 0
        self.immunity_function = immunity_function

    def move(self):

        step_options = self.model.grid.get_neighborhood(self.pos,
                                                        moore=True,
                                                        include_center=False)

        new_pos = self.random.choice(step_options)
        self.model.grid.move_agent(self, new_pos)

    def infection(self):

        self.time_since_inf = 0
        self.status = 1

    def step(self):

        self.move()

        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        infection_prob = self.model.infection_prob

        if self.status == 2:

            self.time_since_recov += 1

            if self.immunity_function(self.time_since_recov) <= random.uniform(0,1):

                self.time_since_recov = 0
                self.status = 0

        for c in cellmates:

            if (random.uniform(0,1) <= infection_prob) and (c.status == 0) and (self.status==1):

                c.infection()
                self.model.step_infected+=1


        if self.status == 1:

            self.time_since_inf += 1

        if self.time_since_inf >= self.model.infection_period:

            if random.uniform(1,1) > .5:
                self.status = 2
                self.time_since_inf = 0
            else:
                self.status = 0






