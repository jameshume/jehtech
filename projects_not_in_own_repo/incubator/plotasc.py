import matplotlib.pyplot as pl
import matplotlib.patches as mpatches

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

class Line:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2


class Pin:
    def __init__(self, p, name):
        self._p = p
        self._name = name

    @property 
    def name(self):
        return self._name

    @property
    def p(self):
        return self._p

class Rectangle:
    def __init__(self, p, w, h):
        self._p = p
        self._w = w
        self._h = h

    @property 
    def p(self):
        return self._p
    
    @property 
    def h(self):
        return self._h
    
    @property 
    def w(self):
        return self._w


class Component:
    def __init__(self, filename):
        self._lines = []
        self._pins  = []
        self._rectangles = []
        self._arcs = []

        state = "idle"
        curret_pin = None

        with open(fn, "r") as fh:
            filecontents = fh.readlines()
            for line in filecontents:
                line =  line.strip()

                while True:
                    if state == "idle":
                        if line[0:len("LINE ")] == "LINE ":
                            line = line.split()[1:]
                            if not represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            self._lines.append(
                                Line(
                                    Point(x1, y1),
                                    Point(x2, y2)
                                )
                            )

                        elif line[0:len("PIN ")] == "PIN ":
                            line = line.split()[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            curret_pin = Pin(x1, y1)
                            state = "pin"

                        elif line[0:len("RECTANGLE ")] == "RECTANGLE ":
                            line = line.split()[1:]
                            if not represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            self._rectangles.append(Rectangle(Point(x1, y1),x2-x1, y2-y1))

                        elif line[0:len("ARC ")] == "ARC ":
                            line = line.split()[1:]
                            if not represents_int(line[0]):
                                line = line[1:]
                            # -20 -124 4 -100 -20 -112 -8 -100
                            a = float(line[0])
                            b = float(line[1])
                            c = float(line[2])
                            d = float(line[3])
                            e = float(line[4])
                            f = float(line[5])
                            g = float(line[6])
                            h = float(line[7])
                            self._arcs.append((a,b,c,d,e,f,g,h))

                    elif state == "pin":
                        if line[0:len("PINATTR ")] == "PINATTR ":
                            line = line.split()[1:]
                            if line[0] == "PinName":
                                self._pins.append(Pin(Point(x1, y1), line[1]))
                                state = "idle"
                        else:
                            state = "idle"
                            continue


                    break # Always break by default.

    @property
    def lines(self):
          return self._lines

    @property 
    def rectangles(self):
        return self._rectangles    

    @property
    def pins(self):
        return self._pins

    @property
    def arcs(self):
        return self._arcs


import numpy as np
import matplotlib.path as mpath
import math

def draw_ltspice_arc(ax,  a, b, c, d, e, f, g, h):

    # (arc4,arc5) and (arc6,arc7) are the points between which the arc should extend. (a,b) looks like the start and (c,d) is the end
    # Define the arc using a Bézier curvea
    # arc0,1 is the boarding box corner and so is arc 2,3
    arc1x = e
    arc1y = f
    arc2x = g
    arc2y = h

    bbox_x1 = a
    bbox_y1 = b
    bbox_x2 = c
    bbox_y2 = d
    bbox_w = bbox_x2 - bbox_x1
    bbox_h = bbox_y2 - bbox_y1
    bbox_xc = bbox_x1 + bbox_w / 2
    bbox_yc = bbox_y1 + bbox_h / 2

    circle1 = pl.Circle((arc1x, arc1y), 1, color='r')
    ax.add_patch(circle1)
    circle1 = pl.Circle((arc2x, arc2y), 1, color='g')
    ax.add_patch(circle1)
    circle1 = pl.Circle((bbox_xc, bbox_yc), 1, color='purple')
    ax.add_patch(circle1)

    # so have to figure out what theta1 and 2 are :/ Thanksyou SO https://math.stackexchange.com/a/613762
    # must convert atan radians to degs.
    # 2pi rad = 360d, 1 rad = 360/2pi
    #
    # Also arc in MPL is drawn counter clockwise. 
    # So when point1 (arcy1,arc1y)

    t1 = math.atan2((bbox_xc - arc1x), (bbox_yc - arc1y)) * 180 / math.pi
    t2 = math.atan2((bbox_xc - arc2x), (bbox_yc - arc2y)) * 180 / math.pi

    print("1", bbox_xc - arc1x, bbox_yc - arc1y)
    print("2", bbox_xc - arc2x, bbox_yc - arc2y)
    print(t1, t2)

    arc1 = mpatches.Ellipse((bbox_xc, bbox_yc), bbox_w, bbox_h, color='yellow', fill=False)
    ax.add_patch(arc1)

    arc1 = mpatches.Arc((bbox_xc, bbox_yc), bbox_w, bbox_h, angle=0, theta1=t1, theta2=t2, color='b')
    ax.add_patch(arc1)



def matplotlib_plot_component(component, ax):
    ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
    ax.set_xticks([]) 
    ax.set_yticks([]) 

    for line in component.lines:
        ax.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], c='b')
    for rect in component.rectangles:
        rect1 = pl.Rectangle((rect.p.x, rect.p.y), rect.w, rect.h, fill=False)
        ax.add_patch(rect1)
    for pin in component.pins:
        circle1 = pl.Circle((pin.p.x, pin.p.y), 1, color='r')
        ax.add_patch(circle1)
        if pin.name is not None:
            ax.text(pin.p.x, pin.p.y, pin.name)
    for arc in component.arcs:
        draw_ltspice_arc(ax, arc[0], arc[1], arc[2], arc[3], arc[4], arc[5], arc[6], arc[7])
        break
        

if False:
    fn = "/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/cap.asy"
    fig, ax = pl.subplots()
    matplotlib_plot_component(Component(fn), ax)
    fig.show()
    pl.show()
    pl.close(fig)

if False:
    fn = "/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/nmos.asy"
    fig, ax = pl.subplots()
    matplotlib_plot_component(Component(fn), ax)
    fig.show()
    pl.show()
    pl.close(fig)

if False:
    fn = "/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/npn.asy"
    fig, ax = pl.subplots()
    matplotlib_plot_component(Component(fn), ax)
    fig.show()
    pl.show()
    pl.close(fig)


fn = "/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/Misc/NE555.asy"
fig, ax = pl.subplots()
matplotlib_plot_component(Component(fn), ax)
fig.show()
pl.show()
pl.close(fig)