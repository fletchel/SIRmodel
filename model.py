from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import SIRAgent

import matplotlib.pyplot as plt

class SIRModel(Model):

    def __init__(self, N, width, height, infection_period, infection_prob, initial_infected):

        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.infection_period = infection_period
        self.infection_prob = infection_prob


        for i in range(self.num_agents):

            agent = SIRAgent(i, self)

            if i < initial_infected:
                agent.infection()

            self.schedule.add(agent)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))



    def step(self):

        self.schedule.step()


def getSIRcurves(N, w, h, ip, iprob, initinf, num_steps):

    test_model = SIRModel(N, w, h, ip, iprob, initinf)

    new_inf = [initinf]
    inf = [initinf]
    sus = [N-initinf]
    recov = [0]

    for i in range(num_steps - 1):

        recovered = 0
        infected = 0
        susceptible = 0

        test_model.step()

        for agent in test_model.schedule.agents:

            if agent.status == 0:
                susceptible = susceptible + 1

            if agent.status == 1:
                infected = infected + 1

            if agent.status == 2:
                recovered = recovered + 1

        sus.append(susceptible)
        inf.append(infected)
        new_inf.append(infected + recovered - inf[i - 1] - recov[i - 1])
        recov.append(recovered)

    plt.plot(range(0, num_steps), new_inf, 'r')
    #plt.plot(range(0, num_steps), sus, 'b')
    #plt.plot(range(0, num_steps), recov, 'g')
    plt.show()

getSIRcurves(2500, 50, 50, 7, 0.4, 10, 75)
