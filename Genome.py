import random
from Hyperparameters import Hyperparameters

class Genome():
    def __init__(self, neat):
        self.neat = neat

        self.connections = []
        self.nodes = []

    def distance(self, g2):
        g1 = self

        highest_innov_g1 = g1.connections[-1].innovation_number if len(g1.connections) > 0 else 0
        highest_innov_g2 = g2.connections[-1].innovation_number if len(g2.connections) > 0 else 0

        if (highest_innov_g1 < highest_innov_g2):
            # swap g1 and g2 (since innov of g1 must be > then g2)
            g1, g2 = g2, g1

        idx_g1 = 0
        idx_g2 = 0

        similar = 0
        disjoint = 0
        excess = 0
        weight_diff = 0

        while idx_g1 < len(g1.connections) and idx_g2 < len(g2.connections):
            con1 = g1.connections[idx_g1]
            con2 = g2.connections[idx_g2]

            in1 = con1.innovation_number
            in2 = con2.innovation_number

            if in1 == in2:
                # same connection gene
                idx_g1 += 1
                idx_g2 += 1
                similar += 1
                weight_diff += abs(con1.weight - con2.weight)
            elif in1 > in2:
                # excess or disjoint gene of b
                idx_g2 += 1
                disjoint += 1
            else:
                # excess or disjoint gene of a
                idx_g1 += 1
                disjoint += 1

        weight_diff /= max(1, similar)
        excess = len(g1.connections) - (idx_g1 + 1)

        # number of genes in the larger genome
        N = max(len(g1.connections), len(g2.connections))
        if N < 20:
            N = 1

        distance = Hyperparameters.C1 * excess / N + Hyperparameters.C2 * \
            disjoint / N + Hyperparameters.C3 * weight_diff
        return distance

    @staticmethod
    def crossOver(genome1, genome2):
        offspring_genome = genome1.neat.empty_genome()

        # genome1 must be better than genome2
        # if genome1.fitness < genome2.fitness: genome1, genome2 = genome2, genome1

        # add all connections
        idx_g1 = 0
        idx_g2 = 0

        while idx_g1 < len(genome1.connections) and idx_g2 < len(genome2.connections):
            con1 = genome1.connections[idx_g1]
            con2 = genome2.connections[idx_g2]

            in1 = con1.innovation_number
            in2 = con2.innovation_number

            if in1 == in2:
                # same connection gene
                idx_g1 += 1
                idx_g2 += 1

                chosen_con = con1 if random.random() > 0.5 else con2
                offspring_genome.connections.append(
                    genome1.neat.copyConnection(chosen_con))

            elif in1 > in2:
                # excess or disjoint gene of b
                idx_g2 += 1

                # don't add excess or disjoint genes of the less fit parent
            else:
                # excess or disjoint gene of a
                idx_g1 += 1

                offspring_genome.connections.append(
                    genome1.neat.copyConnection(con1))

        # add excess genes of a if they exist
        while idx_g1 < len(genome1.connections):
            offspring_genome.connections.append(
                genome1.neat.copyConnection(genome1.connections[idx_g1]))
            idx_g1 += 1

        # add all hidden nodes to the offspring
        # (maybe one parent has created a new node, if its more fit, there are connections from ex. input layer to a hidden layer)
        # based on this connection, add these nodes

        for con in offspring_genome.connections:
            for node in [con.origin, con.target]:
                # check if node already exists inside offspring genome (ex: input/ output node)
                if node not in offspring_genome.nodes:
                    offspring_genome.nodes.append(node)

        return offspring_genome

    # add a link
    def mutate_link(self):
        for _ in range(100):
            a = random.choice(self.nodes)
            b = random.choice(self.nodes)

            if a.x == b.x: continue

            con = None
            if (a.x < b.x): con = self.neat.getConnection(a, b)
            else: con = self.neat.getConnection(b, a)

            # check if connection already exists in this genome (then try to find new nodes)
            conAlreadyExists = False
            for alreadyExistingCons in self.connections:
                if alreadyExistingCons.equals(con):
                    conAlreadyExists = True
                    break
            if conAlreadyExists: continue

            con.weight = (random.random() * 2 - 1) * Hyperparameters.WEIGHT_RANDOM_STRENGTH
            self.connections.append(con)
            self.connections.sort(key=lambda obj: obj.innovation_number)

            break

    # choose a random connection, split it and add a new node in the middle
    # weight of the first link = 1, weight of the second link = the original weight
    def mutate_node(self, con):
        middleNode = self.neat.getNewNode(
            posX = (con.origin.x + con.target.x) / 2,
            posY = (con.origin.x + con.target.x) / 2
        )

        con1 = self.neat.getConnection(con.origin, middleNode)
        con2 = self.neat.getConnection(middleNode, con.target)

        con1.weight = 1
        con2.weight = con.weight
        con2.enabled = con.enabled

        self.connections.remove(con)
        self.connections.append(con1)
        self.connections.append(con2)
        self.nodes.append(middleNode)

    # increase weight by some value
    def mutate_weight_shift(self, con):
        con.weight += Hyperparameters.WEIGHT_SHIFT_STRENGTH

    # set weight to new random value
    def mutate_weight_random(self, con):
        con.weight = (random.random() * 2 - 1) * \
            Hyperparameters.WEIGHT_RANDOM_STRENGTH

    # toggle enabled state
    def mutate_link_toggle(self, con):
        con.enabled = not con.enabled
