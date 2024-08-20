import random
from Neat import Neat
from NNPlotter import Plotter

neat = Neat(3, 3, 1)
client = neat.clients[0]

for con in [(0, 4), (0, 5), (2, 5), (2, 3)]:
    connection = neat.getConnection(
        client.genome.nodes[con[0]],
        client.genome.nodes[con[1]]
    )
    connection.weight = round(random.random(), 3)
    connection.enabled = True
    client.genome.connections.append(connection)

def calculateTest():
    input = [1, 1, 1]
    client.calculator.setup(client.genome)
    output = client.calculate(input)
    print(output)

plotter = Plotter(client, calculateHandler = calculateTest)
plotter.draw()
