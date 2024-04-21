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

def draw_ltspice_arc(ax,  a, b, c, d, e, f, g, h):

    # (a,b) and (c,d) are the points between which the arc should extend. (a,b) looks like the start and (c,d) is the end
    # Define the arc using a Bézier curvea
    circle1 = pl.Circle((e, f), 1.2, color='r')
    ax.add_patch(circle1)
    circle1 = pl.Circle((g, h), 1.2, color='g')
    ax.add_patch(circle1)

    circle1 = pl.Circle((a, b), 1.2, color='purple')
    ax.add_patch(circle1)

    circle1 = pl.Circle((c, d), 1.2, color='b')
    ax.add_patch(circle1)

    #path = mpatches.PathPatch(
    #    mpath.Path([(start_x, start_y), (cp2_x, cp2_y), (end_x, end_y), (cp1_x, cp1_y)], 
    #    [mpatches.Path.MOVETO, mpatches.Path.CURVE3, mpatches.Path.CURVE3, mpatches.Path.STOP]),fc="none")
    
    # Add the arc to the plot
    #ax.add_patch(path)

def matplotlib_plot_component(component, ax):
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
        # -20 -124     4 -100     -20 -112 -8 -100
        #xy, width, height
        #arc1 = mpatches.Arc((arc[0], arc[1]), arc[2]-arc[0], arc[3]-arc[1], theta1=arc[5], theta2=arc[6])
        draw_ltspice_arc(ax, arc[0], arc[1], arc[2], arc[3], arc[4], arc[5], arc[6], arc[7])
        break
        #ax.add_patch(arc1)

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