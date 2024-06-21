import math
import turtle
import argparse

# draw the circle using turtle
def drawCircle(x, y, r):
    # move to the start of circle
    turtle.up()
    turtle.setpos(x+r, y)
    turtle.down()

    # draw the circle
    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x+r*math.cos(a), y+r*math.sin(a))

def main():
    desc_str="""input the center pos and radius of circle."""
    parser = argparse.ArgumentParser(description=desc_str)
    parser.add_argument("x", type=float, help="the x axis of circle center")
    parser.add_argument("y", type=float, help="the y axis of circle center")
    parser.add_argument("r", type=float, help="the radius of circle")
    args = parser.parse_args()
    drawCircle(args.x, args.y, args.r)
    turtle.done()

if __name__ == '__main__':
    main()