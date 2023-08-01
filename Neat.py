import random
from Client import Client
from Hyperparameters import Hyperparameters
from NodeGene import NodeGene
from Genome import Genome
from ConnectionGene import ConnectionGene
from Species import Species
from RandomSelector import RandomSelector

class Neat():
    def __init__(self, input_size, output_size, clients):
        # other attributes
        self.all_connections = []
        self.all_nodes = []

        self.species = []

        self.reset(input_size, output_size, clients)

    def empty_genome(self):
        genome = Genome(self)
        for i in range(self.input_size):
            genome.nodes.append(self.getNewNode(posX = 0.1, posY = 0.1 + 0.8 * i / self.input_size))
        for i in range(self.output_size):
            genome.nodes.append(self.getNewNode(posX = 0.9, posY = 0.1 + 0.8 * i / self.output_size))
        
        return genome

    def reset(self, input_size, output_size, clients):
        self.input_size = input_size
        self.output_size = output_size
        self.max_clients = clients

        self.clients = []
        self.all_nodes = []
        self.all_connections = []

        for i in range(input_size):
            self.getNewNode(posX = 0.1, posY = 0.1 + 0.8 * i / self.input_size)

        for i in range(output_size):
            self.getNewNode(posX = 0.9, posY = 0.1 + 0.8 * i / self.output_size)

        for i in range(self.max_clients):
            client = Client()
            client.genome = self.empty_genome()
            client.setup_calculator()
            self.clients.append(client)


    def getNewNode(self, posX = None, posY = None):
        alreadyExists = next((node for node in self.all_nodes if node.x == posX and node.y == posY), None)
        if alreadyExists: return alreadyExists

        node = NodeGene(len(self.all_nodes))
        node.x = posX
        node.y = posY
        self.all_nodes.append(node)
        return node

    def getNode(self, innovationNumber):
        if innovationNumber < 0 or innovationNumber > len(self.all_nodes): return None
        if innovationNumber == len(self.all_nodes): return self.getNewNode()
        return self.all_nodes[innovationNumber]
    
    def getConnection(self, node1, node2):
        connectionGene = ConnectionGene(node1, node2)

        # check if it already exists
        for existingConnectionGene in self.all_connections:
            if connectionGene.equals(existingConnectionGene):
                connectionGene.innovation_number = existingConnectionGene.innovation_number
                return connectionGene
        
        connectionGene.innovation_number = len(self.all_connections)
        self.all_connections.append(connectionGene)
        return connectionGene
    
    def copyConnection(self, con):
        conCopy = ConnectionGene(con.origin, con.target, weight = con.weight, enabled = con.enabled)
        conCopy.innovation_number = con.innovation_number
        return conCopy

    def evolve(self):
        self.__generate_species()
        self.__kill()
        self.__remove_extinct_species()
        self.__reproduce()
        self.__mutate()

        for c in self.clients: c.setup_calculator()
    
    def __generate_species(self):
        # reset all species (all clients have no species attribute (except the representatives of each species))
        for sp in self.species: sp.reset()
        
        # put all clients back into their corresponding species
        for c in self.clients:
            if c.species != None: continue

            speciesFound = False
            for sp in self.species:
                if sp.addClient(c):
                    speciesFound = True
                    break

            # if there is not fitting species, create a new one       
            if not speciesFound:
                self.species.append(Species(c))
        
        # evaluate score
        for sp in self.species: sp.evaluate_score()

    def __kill(self):
        for sp in self.species: sp.kill(Hyperparameters.PROBABILIY_SURVIVE_KILL_SPECIES)

    def __remove_extinct_species(self):
        species_to_remove = [sp for sp in self.species if len(sp.clients) <= 1]
        for sp in species_to_remove:
            sp.goExtinct()
            self.species.remove(sp)
        
        return [hex(id(sp)) for sp in species_to_remove]
    
    def __reproduce(self):
        for c in self.clients:
            # check if the client was killed (no species)
            # => got killed because score was too bad, breed better networks and assign it on this client
            if c.species == None:
                for _ in range(100):
                    if len(self.species) == 0:
                        print("NO SPECIES LEFT!!")
                    species = RandomSelector.get(self.species)
                    offspring = species.breed()

                    if offspring != None:
                        c.genome = offspring
                        species.forceClient(c)
                        break
    
    def __mutate(self):
        for client in self.clients: client.mutate()

    def print_information(self):
        print("########################################")
        for idx, sp in enumerate(self.species):
            print(f"Species {idx}({hex(id(sp))}) - Score:{round(sp.score, 3)} - Num of Clients: {len(sp.clients)}")
