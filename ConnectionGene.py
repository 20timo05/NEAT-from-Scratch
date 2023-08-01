import random

class ConnectionGene():
    def __init__(self, origin, target, weight = None, enabled = True):
        self.innovation_number = None

        self.origin = origin
        self.target = target

        self.weight = weight
        self.enabled = enabled

        self.percentOfLine = 0.25 if (random.random() > 0.5) else 0.75

    def equals(self, otherConnectionGene):
        if not isinstance(otherConnectionGene, ConnectionGene):
            return False
        matching_origin = self.origin.innovation_number == otherConnectionGene.origin.innovation_number
        matching_target = self.target.innovation_number == otherConnectionGene.target.innovation_number
        return matching_origin and matching_target
