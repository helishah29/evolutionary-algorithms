##### HELI SHAH ##### SU ID: 733914949
##### SUKET SINGH ##### SU ID: 923377656
##### CIS 600 EVOLUTIONARY MACHINE LEARNING
##### COURSEWORK PROJECT
##### TRAVELLING SALESMAN PROBLEM USING ANT COLONY OPTIMIZATION
##### GENETIC ALGORITHM IMPLEMENTATION
##### Python 2.7

import sys
import random
import math
import time
import Tkinter
import threading

#City coordinates dataset

distance_x = [
    178,272,176,171,650,499,267,703,408,437,491,74,532,
    416,626,42,271,359,163,508,229,576,147,560,35,714,
    757,517,64,314,675,690,391,628,87,240,705,699,258,
    428,614,36,360,482,666,597,209,201,492,294]
distance_y = [
    170,395,198,151,242,556,57,401,305,421,267,105,525,
    381,244,330,395,169,141,380,153,442,528,329,232,48,
    498,265,343,120,165,50,433,63,491,275,348,222,288,
    490,213,524,244,114,104,552,70,425,227,331]

# Genetic algorithm
 
from GA import GA

#----------- TSP problem -----------

class MyTSP(object):

    # initialization

    def __init__(self, root, width = 800, height = 600, n = 50):

        # Create canvas

        self.root = root                               
        self.width = width      
        self.height = height
        #The number of cities is initialized to 32

        self.n = n
        # Tkinter.Canvas
        self.canvas = Tkinter.Canvas(
                root,
                width = self.width,
                height = self.height,
                bg = "#000000",             # Background black
 
                xscrollincrement = 1,
                yscrollincrement = 1
            )
        self.canvas.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
        self.title("TSP genetic algorithm (n: random initial e: start evolution s: stop evolution q: exit the program")
        self.__r = 5
        self.__lock = threading.RLock()     # Thread lock


        self.__bindEvents()
        self.new()

    # Button response program

    def __bindEvents(self):

        self.root.bind("q", self.quite)    # exit the program

        self.root.bind("n", self.new)      
        self.root.bind("e", self.evolve)   
        self.root.bind("s", self.stop)     

    #Change title

    def title(self, s):

        self.root.title(s)
            
    # Random initial

    def new(self, evt = None):

        # Stop thread

        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()     # Clear information
 
        self.nodes = []  # Node coordinates

        self.nodes2 = [] # Node object


        # Initialize the city node

        for i in range(len(distance_x)):
            # Random initial coordinates on the canvas

            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x, y))
            # Generate a node ellipse with a radius of self.__r
            node = self.canvas.create_oval(x - self.__r,
                    y - self.__r, x + self.__r, y + self.__r,
                    fill = "#38ff3b",      # Filled with green

                    outline = "#000000",   # Outline black

                    tags = "node",
                )
            self.nodes2.append(node)
            # Display coordinates

            self.canvas.create_text(x,y-10,                
                    text = '('+str(x)+','+str(y)+')',      
                    fill = 'white'                       
                )
            
        # Connecting cities in sequence

        self.line(range(self.n))      
        
        # Genetic algorithm

        self.ga = GA(
                lifeCount = 50,
                xRate = 0.7,
                mutationRate = 0.1,
                judge = self.judge(),
                mkLife = self.mkLife(),
                xFunc = self.xFunc(),
                mFunc = self.mFunc(),
                save = self.save()
            )

    # Get the total length of the connection in the current order

    def distance(self, order):
        
        distance = 0
        for i in range(-1, self.n - 1):
            i1, i2 = order[i], order[i + 1]
            p1, p2 = self.nodes[i1], self.nodes[i2]
            distance += math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        return distance

    # Create new life

    def mkLife(self):
        def f():
            lst = range(self.n)
            # Random order

            random.shuffle(lst)
            return lst
        return f

    # Evaluation function

    def judge(self):
            
        return lambda lf, av = 100: 1.0 / self.distance(lf.gene)

    # Cross function: select the lf2 sequence before the subsequence crosses to the front of lf1, removing the repeating elements

    def xFunc(self):
            
        def f(lf1, lf2):
            p2 = random.randint(1, self.n - 1)
            # Intercept if2

            g1 = lf2.gene[0:p2] + lf1.gene
            g11 = []
            for i in g1:
                if i not in g11:
                    g11.append(i)
            return g11
        return f
        
    # Variant function: Select two different positions for gene exchange, and the first selected gene is rejoined to the end of the sequence.

    def mFunc(self):
            
        def f(gene):
            p1 = random.randint(0, self.n - 1)
            p2 = random.randint(0, self.n - 1)
            while p2 == p1:
                p2 = random.randint(0, self.n - 1)
            gene[p1], gene[p2] = gene[p2], gene[p1]
            gene.append(gene[p2])
            del gene[p2]
            return gene
            
        return f

    # Preservation

    def save(self):
        def f(lf, gen):
            pass
        return f

    # Evolutionary calculation

    def evolve(self, evt = None):

        # Open thread

        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        while self.__running:
            # Next evolution

            self.ga.next()
            #Connection

            self.line(self.ga.best.gene)
            # Set title

            self.title("TSP genetic algorithm (n: random initial e: start evolution s: stop evolution q: exit the program) number of iterations: %d" % self.ga.generation)
            # Update canvas

            self.canvas.update()
            print("Number of iterations: %d, number of variations %d, total path total distance: %d" % (self.ga.generation, self.ga.mutationCount, self.distance(self.ga.best.gene))) 

    # Wire nodes in order

    def line(self, order):
        # Delete the original line

        self.canvas.delete("line")
        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill = "#fc3535", tags = "line")
            return i2
        
        # order[-1]Initial value

        reduce(line2, order, order[-1])

    # Clear canvas

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    # exit the program

    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print u"\n program has been quit..."
        sys.exit()

    # Stop evolution

    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

    # Main loop

    def mainloop(self):
        self.root.mainloop()

#----------- Entrance to the program -----------
        
if __name__ == "__main__":
    

    
    MyTSP(Tkinter.Tk()).mainloop()
