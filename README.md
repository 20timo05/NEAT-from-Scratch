# Implementation of NEAT (Neuroevolution of augmenting topologies) from Scratch

# Motivation
[NEAT](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.28.5457&rep=rep1&type=pdf) is an effective algorithm for AI's to learn to play video games. The motivation for this project was to actually understand NEAT, before using the algorithm to learn to play video games by using some library like [NEAT-Python](https://neat-python.readthedocs.io/en/latest/).
This program should in theory be able to be used in place of this library or even general purpose AI libraries like [Tensorflow](https://www.tensorflow.org/) or [Pytorch](https://pytorch.org/) and will be tested in the future.
During the development of this project, I learned a lot about the actual details of how NEAT works, but it was also a good practice to learn python (as a primary JavaScript developer).

# Credits
This project was created alongside this [Explanation Series](https://youtube.com/playlist?list=PLgomWLYGNl1fcL0o4exBShNeCC5tc6s9C). Since I am using Python instead of Java, the code differs from the original (also because many bugs have been fixed by me).

# How to run the project
Currently there are two files to test the project: testGenome.py and testEvolve.py.

testGenome.py creates a Genome (Neural Network) with some default connections and opens a window, visualizing this Genome. It also has an interface where one can mutate the Genome manually and test it by calculating some output based on the input hard-coded in the file.

testEvolve.py shows how the program could actually be used to learn a specific task. In this case, the AI is rewarded for generating a high output. In practice, instead of just setting the score to the output of the Genome, one would have to test the Genome in an environment, calculate some Fitness-Value and then start the evolving process. However this somehow pointless implementation still shows that the Algorithm is working as many species approch a score of 1 (maximum, since the [Sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function) function was used on the output). 
