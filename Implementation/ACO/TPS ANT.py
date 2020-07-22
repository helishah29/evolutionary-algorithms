##### HELI SHAH ##### SU ID: 733914949
##### SUKET SINGH ##### SU ID: 923377656
##### CIS 600 EVOLUTIONARY MACHINE LEARNING
##### COURSEWORK PROJECT
##### TRAVELLING SALESMAN PROBLEM USING ANT COLONY OPTIMIZATION
##### ACO IMPLEMENTATION
##### Python 2.7

import random
import copy
import time
import sys
import math
import Tkinter
import threading

# parameter

(ALPHA, BETA, RHO, Q) = (1.0,2.0,0.5,100.0)

# City number, ant colony

(city_num, ant_num) = (50,50)

# City coordinates

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

# City distance and pheromone

distance_graph = [ [0.0 for col in xrange(city_num)] for raw in xrange(city_num)]
pheromone_graph = [ [1.0 for col in xrange(city_num)] for raw in xrange(city_num)]

#-----------ant -----------
class Ant(object):

    # initialization

    def __init__(self,ID):
        
        self.ID = ID                 # ID
        self.__clean_data()          # Randomly initialize the birth point

    # Initial data

    def __clean_data(self):
    
        self.path = []               # Current ant's path
         
        self.total_distance = 0.0    # Total distance of the current path

        self.move_count = 0          # Number of moves

        self.current_city = -1       # Current city

        self.open_table_city = [True for i in xrange(city_num)] # Explore the state of the city

        
        city_index = random.randint(0,city_num-1) # Random initial birth point

        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1
    
    # Choose the next city

    def __choice_next_city(self):
        
        next_city = -1
        select_citys_prob = [0.0 for i in xrange(city_num)]
        total_prob = 0.0

        # Get the probability of going to the next city

        for i in xrange(city_num):
            if self.open_table_city[i]:
                try :
                    # Calculated probability: proportional to pheromone concentration, inversely proportional to distance

                    select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow((1.0/distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError, e:
                    print 'Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID = self.ID, current = self.current_city, target = i)
                    sys.exit(1)
        
        # Roulette selection city

        if total_prob > 0.0:
            # Generate a random probability

            temp_prob = random.uniform(0.0, total_prob)
            for i in xrange(city_num):
                if self.open_table_city[i]:
                    # Round subtraction

                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break
                    
        # No probability is generated, order an unvisited city
            
        if next_city == -1:
            for i in xrange(city_num):
                if self.open_table_city[i]:
                    next_city = i
                    break
                
        # Return to the next city serial number

        return next_city
    
    # Calculate the total distance of the path

    def __cal_total_distance(self):
        
        temp_distance = 0.0
        
        for i in xrange(1, city_num):
            start, end = self.path[i], self.path[i-1]
            temp_distance += distance_graph[start][end]

        # circuit
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance
        
    
    # Mobile operation

    def __move(self, next_city):
        
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1
        
    # Search path

    def search_path(self):

        # Initialization data

        self.__clean_data()

        # Search for the path, traversing all cities

        while self.move_count < city_num:
            # Move to the next city

            next_city =  self.__choice_next_city()
            self.__move(next_city)

        # Calculate the total length of the path

        self.__cal_total_distance()

#----------- TSP problem-----------
        
class TSP(object):

    def __init__(self, root, width = 800, height = 600, n = city_num):

        # Create canvas

        self.root = root                               
        self.width = width      
        self.height = height
        # The number of cities is initialized to city_num
        self.n = n
        # Tkinter.Canvas
        self.canvas = Tkinter.Canvas(
                root,
                width = self.width,
                height = self.height,
                bg = "#000000",     # Background black
 
                xscrollincrement = 1,
                yscrollincrement = 1
            )
        self.canvas.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
        self.title("TSP ant colony algorithm (n: initialization e: start search s: stop search q: exit the program)")
        self.__r = 5
        self.__lock = threading.RLock()     # Thread lock


        self.__bindEvents()
        self.new()

        # Calculate the distance between cities

        for i in xrange(city_num):
            for j in xrange(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))

    # Button response program

    def __bindEvents(self):

        self.root.bind("q", self.quite)        # exit the program

        self.root.bind("n", self.new)          # initialization

        self.root.bind("e", self.search_path)  # Start searching

        self.root.bind("s", self.stop)         # Stop searching

    # Change title

    def title(self, s):

        self.root.title(s)

    # initialization

    def new(self, evt = None):

        # Stop thread

        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()     
        self.nodes = []          
        self.nodes2 = [] 

        # Initialize the city node

        for i in range(len(distance_x)):
            # Random initial coordinates on the canvas

            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x, y))
            #Generate a node ellipse with a radius of self.__r
            node = self.canvas.create_oval(x - self.__r,
                    y - self.__r, x + self.__r, y + self.__r,
                    fill = "#38ff3b",      # Filled with green

                    outline = "#000000",   # Outline black

                    tags = "node",
                )
            self.nodes2.append(node)
            # Display coordinates

            self.canvas.create_text(x,y-10,              # Use the create_text method to draw text at coordinates (302, 77)

                    text = '('+str(x)+','+str(y)+')',    #The content of the drawn text
 
                    fill = 'white'                       # The color of the drawn text is gray

                )
            
        # Connecting cities in sequence

        #self.line(range(city_num))
        
        # Distance between the initial cities and pheromones

        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone_graph[i][j] = 1.0
                
        self.ants = [Ant(ID) for ID in xrange(ant_num)]  #Initial ant colony

        self.best_ant = Ant(-1)                          # Initial optimal solution

        self.best_ant.total_distance = 1 << 31           # Initial maximum distance

        self.iter = 1                                    # Initialization iteration distance
 
            
    # Wire nodes in order

    def line(self, order):
        # Delete the original line
        self.canvas.delete("line")
        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill = "#fc3535", tags = "line")
            return i2
        
        # Order[-1] is the initial value

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
        print u"\nThe program has quit..."
        sys.exit()

    #Stop searching

    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        
    # Start searching

    def search_path(self, evt = None):

        # Open thread

        self.__lock.acquire()
        self.__running = True
        self.__lock.release()
        
        while self.__running:
            # Traversing each ant

            for ant in self.ants:
                # Search for a path

                ant.search_path()
                # Compared with current optimal ants

                if ant.total_distance < self.best_ant.total_distance:
                    #Update optimal solution

                    self.best_ant = copy.deepcopy(ant)
            # Update pheromone

            self.__update_pheromone_gragh()
            print u"Number of iterations: ", self.iter, u" the best path total distance: ", int(self.best_ant.total_distance)

            # Connection

            self.line(self.best_ant.path)
            # Set title

            self.title("TSP ant colony algorithm (n: random initial e: start search s: stop search q: exit the program) number of iterations: %d" % self.iter)

            # Update canvas

            self.canvas.update()
            self.iter += 1

    # Update pheromone

    def __update_pheromone_gragh(self):

        # Get the pheromone left by each ant on its path

        temp_pheromone = [[0.0 for col in xrange(city_num)] for raw in xrange(city_num)]
        for ant in self.ants:
            for i in xrange(1,city_num):
                start, end = ant.path[i-1], ant.path[i]
                # Leave a pheromone between every two adjacent cities on the path, inversely proportional to the total distance of the path
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # Update pheromones between all cities, old pheromone attenuation plus new iterative pheromones

        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]

    # Main loop

    def mainloop(self):
        self.root.mainloop()

#----------- Entrance to the program-----------
                
if __name__ == '__main__':
    TSP(Tkinter.Tk()).mainloop()
    
