from math import floor, sqrt, sin, cos, pi 

#a neighbourhood is a function like
#hexagonal = lambda x, y : [(x - 1, y - 1), . . .]
#i.e with x, y as input (exploded pt), returns a list of tuples
    
def spiral(n):
    #inspired implementation
    x, y = 0, 0 
    for i in range(n):
        angle = (floor(sqrt(4 * i + 1)) - 1) * pi / 2
        x = int(x - cos(angle))   
        y = int(y - sin(angle))  
        yield (x, y)


def from_coords(coords):
    #evil use of eval for a small (?) performance increase
    evalstr = "lambda x, y : [%s]" % ','.join(["(x + %i, y + %i)" % pt for pt in coords])
    return eval(evalstr)


def bin_to_coords(binstr):
    length = len(binstr)
    return [pt for idx, pt in enumerate(spiral(length)) if binstr[length - idx - 1] == "1"]


def int_to_coords(n):
    return bin_to_coords(bin(n)[2 : ])


def from_bin(binstr):
    #take binary as a string, e.g "1010"
    #yield coords from a spiral by "1" iterating backwards
    return from_coords(bin_to_coords(binstr))


def from_int(n):
    #e.g from_int(119) = from_bin("01110111") -> hexagonal adjacency
    return from_coords(int_to_coords(n))


def _transitions_from_int(n):
    #golly stores rule files with their transitions explicit, as in
    #c, n,ne,e,se,s,sw,w,nw, c'
    #i.e. a cell in state c transitions to state c' if the cells in n,ne, . . ., are as desired
    #this function makes the above transitions; boilerplate filled out elsewhere 

    assert n < 256  #golly limited to subsets of the moore neighbourhood
    
    asbin = bin(n)[2 : ].zfill(8)

    #we want to match the nbhds produced by spiral which requires a circular bit shift to the left
    asbin = asbin[1 : ] + asbin[0] 
    
    indices = [i for i in range(8) if asbin[i] == "1"]
    func = lambda arr : sum([arr[idx] == "1" for idx in indices]) == 1
    t = [bin(i)[2 : ].zfill(8) for i in range(256)]
    t = [i for i in t if func(i)]
    return '\n'.join(["0, {}, 1".format(','.join(list(i))) for i in t])


def rule_from_int(n, rulename):
    trans = _transitions_from_int(n)
    filedata = f"@RULE {rulename}\n@TABLE\nn_states:2\nneighborhood:Moore\nsymmetries:none\n\n{trans}"
    with open(f"{rulename}.rule", "w") as f:
        f.write(filedata)
    





