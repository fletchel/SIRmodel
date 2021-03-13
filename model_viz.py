from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import SIRModel

def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Color": "blue",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.6}

    if agent.status == 1:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1

    if agent.status == 2:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 2

    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 1000, 1000)

server = ModularServer(SIRModel, [grid], "SIR Model", {"N":5000, "width":50,
                                                       "height":50, "infection_prob":0.1,
                                                       "infection_period":10, "initial_infected":5})

server.port=8521
server.launch()