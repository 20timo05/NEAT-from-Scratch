class NodeGene():
    def __init__(self, innovation_number):
        self.innovation_number = innovation_number

        self.x = None
        self.y = None
    
    # check if this NodeGene equals another NodeGene
    def equals(self, otherNodeGene):
        if not isinstance(otherNodeGene, NodeGene): return False
        return self.innovation_number == otherNodeGene.innovation_number
    
