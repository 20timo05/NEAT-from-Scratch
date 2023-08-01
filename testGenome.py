import random
from Neat import Neat
from NNPlotter import Plotter

neat = Neat(3, 3, 100)
genome = neat.empty_genome()

for con in [(0, 4), (0, 5), (2, 5), (2, 3)]:
    connection = neat.getConnection(
        genome.nodes[con[0]],
        genome.nodes[con[1]]
    )
    connection.weight = round(random.random(), 3)
    connection.enabled = True
    genome.connections.append(connection)

def calculateTest():
    input = [1, 1, 1]
    genome.calculator.setup(genome)
    output = genome.calculator.calculate(input)
    print(output)

plotter = Plotter(genome, calculateHandler = calculateTest)
plotter.draw()
