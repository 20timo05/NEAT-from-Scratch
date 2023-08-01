import random
from Neat import Neat


neat = Neat(10, 1, 1000)
input = [random.random() for _ in range(10)]

for generation in range(100):
  for c in neat.clients:
      output = c.calculate(input)
      
      # get score based on output
      c.score = output[0]

  neat.evolve()

  neat.print_information()