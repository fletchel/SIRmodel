from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import SIRModel
import numpy as np

def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Color": "blue",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.6}

    if agent.status == 1:
        portrayal["Color"] = "red"
        portrayal["r"] = 0.7
        portrayal["Layer"] = 1

    if agent.status == 2:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5

    return portrayal


grid = CanvasGrid(agent_portrayal, 40, 40, 1000, 1000)

server = ModularServer(SIRModel, [grid], "SIR Model", {"N":1600, "width":40,
                                                       "height":40, "infection_prob":0.28,
                                                       "infection_period":10, "initial_infected":5, "immunity_function":lambda x: np.exp(-0.0002*x)})

#server.port=8521
#server.launch()
