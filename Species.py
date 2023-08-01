
import random
from Genome import Genome
from Hyperparameters import Hyperparameters
from RandomSelector import RandomSelector

class Species():
    def __init__(self, representative):
        representative.species = self

        self.clients = [representative]
        self.representative = representative
        self.score = None
    
    def addClient(self, newClient):
        if newClient.distance(self.representative.genome) < Hyperparameters.MAX_SPECIES_DISTANCE:
          newClient.species = self
          self.clients.append(newClient)
          return True
        
        return False
    
    def forceClient(self, newClient):
        newClient.species = self
        self.clients.append(newClient)
    
    def goExtinct(self):
        for client in self.clients: client.species = None

    def evaluate_score(self):
        total_score = sum(client.score for client in self.clients)
        avg_score = total_score / len(self.clients)
        self.score = avg_score
    
    def reset(self):
        self.representative = random.choice(self.clients)
        self.goExtinct()
        self.clients = [self.representative]
        self.representative.species = self
        self.score = 0
    
    def kill(self, keepPerc):
        # sort clients by score
        sortedClients = sorted(self.clients, key=lambda client: client.score, reverse=True)
        
        # Calculate the number of clients to keep based on the keepPerc
        num_to_keep = max(1, int(len(sortedClients) * keepPerc))

        # kill fraction of this species (keep num_to_keep)
        for c in sortedClients[num_to_keep:]: c.species = None
        self.clients = sortedClients[:num_to_keep]
    
    def breed(self):
        if len(self.clients) <= 1: return None

        c1 = RandomSelector.get(self.clients)
        c2 = RandomSelector.get(self.clients)

        if c2.score > c1.score: c1, c2 = c2, c1
        offspring = Genome.crossOver(c1.genome, c2.genome)

        return offspring
    
    