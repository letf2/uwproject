from nbhds import *
#class for doing the raw iteration
#few extra bells and whistles for convenience, imaging purposes
#supports a boundary condition - useful for analysis, n-triangles



class UWAutomaton:


    def __init__(self, nbhd, boundary=lambda x, y : True, initial=[(0, 0)], exclude_pt_history=False):
        self.nbhd = nbhd  #i.e lambda x, y : [(x + 1, y), (x, y + 1)] yields a sierpienski gasket
        self.boundary = boundary  #restriction on creation of new cells
        self.initial = initial
        self.exclude_pt_history = exclude_pt_history  #whether or not to save the generation number (or some other statistic) of every pt; only a marginal slowdown
        
        self.reset()
        
    
    def reset(self):
        #return everything to initial conditions
        self.alive = set(self.initial)  #black cells

        #cells which were passed over in a previous iteration
        #in this case that means having more than 1 neighbour
        #since no. of neighbours is increasing, such cells can never be born
        self.dead = set()
        
        self.new = set(self.initial)  #cells whose neighbours we investigate in the iteration

        self.iteration = 1  #1-indexed
        self.history = {1 : len(self.initial)}

        if not self.exclude_pt_history:
            self.pt_history = {pt : 1 for pt in self.initial}

    
    def _iterate(self):
        #excessive hashing of pts might result in slowdown ? investigate
        new = set()
        
        for pt1 in self.new:
            #for each cell that was born on the last generation . . . 
            for pt2 in self.nbhd(*pt1):
                #for each neighbour of that cell . . .
                if self.boundary(*pt2) and not pt2 in self.alive and not pt2 in self.dead:
                    #must be in the boundary region
                    #must not be in alive, since that is a cell already born/passed over
                    if pt2 in new:  #cell has at least one other neighbour
                        new.remove(pt2)  #pt2 will no longer be born
                        self.dead.add(pt2)  #mark pt2 as passed over
                    else:
                        new.add(pt2)

        #add new cells to be born to set of all alive cells
        self.alive.update(new)
        self.new = new
        
        self.iteration += 1
        self.history[self.iteration] = len(self.alive)

        if not self.exclude_pt_history:
            for pt in new:
                self.pt_history[pt] = self.iteration

        
    def goto(self, n):
        if n < self.iteration:
            #could improve by caching last x generations, last complete generations, . . . 
            self.reset()
            self.iterate(n - 1)
        else:
            self.iterate(n - self.iteration)


    def iterate(self, n=1):
        for _ in range(n):
            self._iterate()


    def complete(self):
        #will only terminate by itself if automaton is bounded
        while len(self.new) != 0:
            self.iterate()



class NTriangle(UWAutomaton):


    def __init__(self, n, nbhd=from_int(119), auto=True):
        super().__init__(nbhd, lambda x, y: 0 <= x <= y <= n, initial=[(0, n), (n, n)]) 
        self.n = n
        
        if auto:
            self.complete()
