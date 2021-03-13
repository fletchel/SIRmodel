from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import SIRAgent
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from scipy.signal import savgol_filter


import numpy as np

class SIRModel(Model):

    def __init__(self, N, width, height, infection_period, infection_prob, initial_infected, immunity_function=lambda x: 1):

        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.infection_period = infection_period
        self.infection_prob = infection_prob

        self.step_infected = 0

        self.immunity_function = immunity_function


        for i in range(self.num_agents):

            agent = SIRAgent(i, self, immunity_function=self.immunity_function)

            if i < initial_infected:
                agent.infection()

            self.schedule.add(agent)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))



    def step(self):

        self.schedule.step()

def moving_average(data, period):

    weights = np.ones(period)/period
    conv = np.convolve(data, weights, mode='same')
    return conv



def getSIRcurves(N, w, h, ip, iprob, initinf, num_steps, immunity_function=lambda x: 1):

    test_model = SIRModel(N, w, h, ip, iprob, initinf, immunity_function=immunity_function)

    new_inf = [initinf]
    inf = [initinf]
    sus = [N-initinf]
    recov = [0]
    R0 = [0]

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

        if inf[i-1] != 0:
            R0.append((ip*test_model.step_infected / (inf[i - 1])))

        else:
            R0.append(0)

        test_model.step_infected = 0

        sus.append(susceptible)
        inf.append(infected)
        new_inf.append(abs(sus[i] - sus[i-1]) - (abs(inf[i] - inf[i-1])) + abs(recov[i]-recov[i-1]))
        recov.append(recovered)

    sus = np.array(sus)
    new_inf = np.array(new_inf)
    recov = np.array(recov)

    R0 = moving_average(R0, 3)

    new_inf = moving_average(new_inf, 3)

    _, ax1 = plt.subplots()

    #ax1.set_ylabel("R0")
    #ax1.plot(range(0, num_steps), R0, 'black')
    #ax1.axhline(y=1)
    ax2 = ax1.twinx()

    ax1.plot(range(0, num_steps), new_inf, 'r', label="New infections")
    ax2.plot(range(0, num_steps), sus/N, 'b', label="Proportion susceptible")
    ax2.plot(range(0, num_steps), recov/N, 'g', label="Proportion immune/recovered")

    ax1.set_ylabel("New infections")
    ax2.set_ylabel("Proportion of Population")

    _.legend(loc="upper right")

    plt.show()

getSIRcurves(1600, 40, 40, 10, 0.25, 5, 400, immunity_function=lambda x: np.exp(-0.001*x))

