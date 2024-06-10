import numpy as np
from math import log
from PIL import Image
from matplotlib import colormaps



def save_img(img, path):
    pill = Image.fromarray(img, "RGBA")
    pill.save(path)


def draw_img(img, axes):
    return axes.imshow(img)



#alternative to this is smth like cmap = lambda UWAutomaton : lambda pt : (0, 0, 0, 255) 
#which works but is cluttered. neater as classes imho
#may be an abuse of OOP.



class LogPeriodic:


    def __init__(self, automaton):
        self.automaton = automaton
        self.viridis = matplotlib.colormaps['viridis']
        

    def __call__(self, pt):
        return self.viridis(log(max(self.automaton.pt_history[pt] - 1, 1), 2) % 1, bytes=True)
            


class Black:


    def __init__(self, automaton):
        self.automaton = automaton


    def __call__(self, pt):
        return (0, 0, 0, 255)
        


class Inker:


    def __init__(self, cmap=Black):
        self.cmap = cmap


    def make_empty_img(self, width, height):
        return np.full((height, width, 4), 0, dtype=np.uint8)  #transparent RGBA easiest to work with


    def make_img(self, automaton):
        #instantiate the cmap on the automaton
        cmap = self.cmap(automaton)
        pts = automaton.alive

        #tightest SQUARE which fits the pts
        x, y = zip(*pts)
        translate = max([-min(x), -min(y), max(x), max(y)])
        width = 2 * translate + 1
        
        img = make_empty_img(width, width)

        transform = np.array([[0, -1], [1, 0]])  #cartesian -> image co-ords
        
        for pt in pts:
            mapped = transform @ pt + translate  #translate broadcasted so no worries
            img[mapped[0], mapped[1]] = cmap(pt)  #nicer notation errors out on my laptop but not on my home PC

        return img


    def save(self, path):
        save_img(make_img(automaton), path)


    def draw(self, axes):
        draw_img(make_img(automaton), axes)




