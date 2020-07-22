

import random

#----------- Life -----------

class Life(object):

    # initialization

    def __init__(self, env, gene = None):

        # Genetic algorithm

        self.env = env

        # Vital gene

        if gene == None:
            self.__rndGene()
        elif type(gene) == type([]):
            self.gene = []
            for k in gene:
                self.gene.append(k)
        else:
            self.gene = gene

    # Randomly initialized gene

    def __rndGene(self):
        self.gene = ""
        for i in range(self.env.geneLength):
            self.gene += str(random.randint(0, 1))

    # Set evaluation score

    def setScore(self, v):
        self.score = v

    # Increase evaluation score

    def addScore(self, v):
        self.score += v
