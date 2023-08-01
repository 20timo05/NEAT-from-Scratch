import random
from Hyperparameters import Hyperparameters
from calculations.Calculator import Calculator

class Client():
    def __init__(self):
        self.genome = None
        self.score = 0
        self.species = None

    def setup_calculator(self):
        self.calculator = Calculator(self.genome)
    
    def calculate(self, input):
        if self.calculator == None:
            self.setup_calculator()
        return self.calculator.calculate(input)

    def distance(self, otherGenome):
        return self.genome.distance(otherGenome)

    def mutate(self, choice = None):
        # [probability, method, needsConnection]
        mutation_options = [
            [Hyperparameters.PROBABILITY_MUTATE_WEIGHT_RANDOM, self.genome.mutate_weight_random, True],
            [Hyperparameters.PROBABILITY_MUTATE_WEIGHT_SHIFT, self.genome.mutate_weight_shift, True],
            [Hyperparameters.PROBABILITY_MUTATE_LINK, self.genome.mutate_link, False],
            [Hyperparameters.PROBABILITY_MUTATE_NODE, self.genome.mutate_node, True],
            [Hyperparameters.PROBABILITY_MUTATE_TOGGLE_LINK, self.genome.mutate_link_toggle, True],
        ]

        if choice == None:
            # get random connection & node
            con = random.choice(self.genome.connections) if len(self.genome.connections) > 0 else None
            if con == None:
                # choose mutation that does not require a connection (only mutate_link)
                filtered_mutation_options = [opt for opt in mutation_options if not opt[2]]
                mutation_options = filtered_mutation_options

            for prob, mutation, needsCon in mutation_options:
                if prob > random.random():
                    if needsCon: mutation(con)
                    else: mutation()

        else: mutation_options[choice][1](*mutation_options[choice][2])