import turtle
import math
from PIL import Image

def get_x(R, k, l, a):
    """ calculate x according the formula """
    x = R * ((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
    return x

def get_y(R, k, l, a):
    """ calculate y according the formula """
    y = R * ((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
    return y

# a class that draws a spiro graph
class Spiro:
    # constructor
    def __init__(self, xc, yc, col, big_r, r, l):
       # create the turtle object
       self.t = turtle.Turtle()
       # set the cursor shape
       self.t.shape("turtle") 
       # set the step in degree
       self.step = 5
       # set the drawing complete flag
       self.drawComplete = False
       # set the parameters
       self.set_params(xc, yc, col, big_r, r, l)
       # initialize the drawing
       self.restart()

    def set_params(self, xc, yc, col, big_r, r, l):
        """set the parameters"""
        # the Spirograph parameters
        self.xc = xc
        self.yc = yc
        self.big_r = int(big_r)
        self.r = int(r)
        self.l = l
        self.col = col
        # reduce r/big_r to its smallest form by dividing with the GCD
        gcd_val = math.gcd(self.r, self.big_r)
        self.nRot = self.r//gcd_val
        # get ratio of radii
        self.k = r/float(big_r)
        # set the color
        self.t.color(col)
        # store the current angle
        self.a = 0

    def restart(self):
        """ restart the drawing"""
        # set the flag
        self.drawComplete = False
        # show the turtle
        self.t.showturtle()
        # go to the first point
        self.t.up()
        big_r, k, l = self.big_r, self.k, self.l
        a = 0.0
        x = get_x(big_r, k, l, a)
        y = get_y(big_r, k, l, a)
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        """ draw the spiro"""
        # draw the rest of the points
        big_r, k, l = self.big_r, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = get_x(big_r, k, l, a)
            y = get_y(big_r, k, l, a)
            self.t.goto(self.xc + x, self.yc + y)
        # drawing is now done, so hide the turtle cursor
        self.t.hideturtle()

    def update(self):
        """ update by one step"""
        # skip the rest of the steps if done
        if self.drawComplete:
            return
        # increment the angle
        self.a += self.step
        # draw a step
        big_r, k, l = self.big_r, self.k, self.l
        a = math.radians(self.a)
        x = get_x(big_r, k, l, a)
        y = get_y(big_r, k, l, a)
        self.t.setpos(self.xc + x, self.yc + y)
        # if drawing is complete, set the flag
        if self.a >= 360*self.nRot:
            self.drawComplete = True
            self.t.hideturtle()

def main():
    spiro = Spiro(0, 0, 'red', 220, 65, 0.8)
    spiro.draw()
    turtle.done()

if __name__ == '__main__':
    main()