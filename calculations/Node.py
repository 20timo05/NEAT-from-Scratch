import math

class Node():
    def __init__(self, x):
        self.x = x
        self.output = None
        self.connections = []

    def calculate(self):
        # calculate weighted sum (input for node)
        sum = 0
        for con in self.connections:
            if con.enabled:
                sum += con.origin.output * con.weight

        # activation function (sigmoid)
        activation = 1 / (1 + math.exp(-sum))

        self.output = activation
