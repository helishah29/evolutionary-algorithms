# -*- coding: utf-8 -*-

import random

# Life class

from Life import Life

#----------- Genetic Algorithm -----------

class GA(object):

    # initialization
    def __init__(self, xRate = 0.7, mutationRate = 0.005, lifeCount = 50, geneLength = 50, judge = lambda lf, av: 1, save = lambda: 1, mkLife = lambda: None, xFunc = None, mFunc = None):
        self.xRate = xRate                                   
        self.mutationRate = mutationRate                    
        self.mutationCount = 0                              
        self.generation = 0                                         
        self.lives = []                                     
        self.bounds = 0.0                                      
        self.best = None                                    
        self.lifeCount = lifeCount                          
        self.geneLength = geneLength                        
        self.__judge = judge                                
        self.save = save                                    
        self.mkLife = mkLife                                
        self.xFunc = (xFunc, self.__xFunc)[xFunc == None]   
        self.mFunc = (mFunc, self.__mFunc)[mFunc == None]   

        # Creating a life set

        for i in range(lifeCount):
            self.lives.append(Life(self, self.mkLife()))

    # Default cross function

    def __xFunc(self, p1, p2):
        
        r = random.randint(0, self.geneLength)
        gene = p1.gene[0:r] + p2.gene[r:]
        return gene
    
    # Default mutation function

    def __mFunc(self, gene):
        
        r = random.randint(0, self.geneLength - 1)
        gene = gene[:r] + ("0", "1")[gene[r:r] == "1"] + gene[r + 1:]
        return gene

    # Produce offspring

    def __bear(self, p1, p2):

        # cross
        r = random.random()
        if r < self.xRate:
            gene = self.xFunc(p1, p2)
        else:
            gene = p1.gene

        # mutation

        r = random.random()
        if r < self.mutationRate:
            gene = self.mFunc(gene)
            self.mutationCount += 1

        # Return to the living body

        return Life(self, gene)

    # According to the score situation, randomly obtain an individual, the probability is proportional to the individual's score attribute

    def __getOne(self):
        # Roulette
        r = random.uniform(0, self.bounds)
        for lf in self.lives:
            r -= lf.score;
            if r <= 0:
                return lf
    # Generate new offspring

    def __newChild(self):
        
        return self.__bear(self.__getOne(), self.__getOne())

    # According to the incoming method f, find the optimal life and life set points

    def judge(self, f = lambda lf, av: 1):
        # The average score

        lastAvg = self.bounds / float(self.lifeCount)
        self.bounds = 0.0
        self.best = Life(self)
        self.best.setScore(-1.0)
        for lf in self.lives:
            lf.score = f(lf, lastAvg)
            if lf.score > self.best.score:
                self.best = lf
            self.bounds += lf.score
            
    # Evolution to the next n generation

    def next(self, n = 1):
        
        while n > 0:
            # Evaluation group

            self.judge(self.__judge)
            # New life collection

            newLives = []
            newLives.append(Life(self, self.best.gene))  # Join the best parents in the competition

            # Generating new life set individuals

            while (len(newLives) < self.lifeCount):
                newLives.append(self.__newChild())
            # Update new life set

            self.lives = newLives
            self.generation += 1
            self.save(self.best, self.generation)

            n -= 1
