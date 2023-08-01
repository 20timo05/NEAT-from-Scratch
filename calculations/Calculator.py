from calculations.Node import Node
from calculations.Connection import Connection

class Calculator():
    def __init__(self, genome):
        self.setup(genome)
    
    def setup(self, genome):
        self.genome = genome

        self.input_nodes = []
        self.hidden_nodes = []
        self.output_nodes = []

        self.all_nodes = {}
        for n in genome.nodes:
            node = Node(n.x)

            if n.x <= 0.1: self.input_nodes.append(node)
            elif n.x >= 0.9: self.output_nodes.append(node)
            else: self.hidden_nodes.append(node)

            self.all_nodes[n.innovation_number] = node

        # sort hidden nodes based on x value
        self.hidden_nodes.sort(key=lambda obj: obj.x)

        for c in genome.connections:
            # find origin and target calculation nodes (based on innovation_number)
            origin = self.all_nodes[c.origin.innovation_number]
            target = self.all_nodes[c.target.innovation_number]
            
            con = Connection(origin, target)
            con.weight = c.weight
            con.enabled = c.enabled

            target.connections.append(con)
    
    def calculate(self, input):
        if len(input) != len(self.input_nodes): raise ValueError(f"Input data shape ({len(input)}) does not match the number of input nodes ({self.input_nodes}).")

        for idx, input_node in enumerate(self.input_nodes):
            input_node.output = input[idx]

        for n in self.hidden_nodes: n.calculate()
        for n in self.output_nodes: n.calculate()
        output = list(map(lambda obj: obj.output, self.output_nodes))

        return output
