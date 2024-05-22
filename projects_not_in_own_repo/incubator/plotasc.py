import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import math
from shapes import LTPoint, LTRectangle, LTArc


#######################################################################################################################
def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True



#######################################################################################################################
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __add__(self, point):
        return Point(self._x + point._x, self._y + point._y)

    def __sub__(self, point):
        return Point(self._x - point._x, self._y - point._y)
    
    def __truediv__(self, scale):
        return  Point(self._x / scale, self._y / scale)

    def __str__(self):
        return f"<{self._x}, {self._y}>"

    def clone(self):
        return Point(self._x, self._y)

    def abs(self):
        return Point(math.fabs(self._x), math.fabs(self._y))

    def rotate(self, degrees):
        rads = (math.pi / 180.0) * degrees
        return Point(
            (self._x * math.cos(rads)) - (self._y * math.sin(rads)),
            (self._y * math.cos(rads)) + (self._x * math.sin(rads))
        )
    
    def as_tuple(self):
        return (self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    


#######################################################################################################################
class Arc:
    def __init__(self, bbox1 : Point, bbox2 : Point, arc1 : Point, arc2 : Point):
        self._bbox1 = bbox1
        self._bbox2 = bbox2
        self._arc1  = arc1
        self._arc2  = arc2

    @property
    def bbox1(self):
        return self._bbox1

    @property
    def bbox2(self):
        return self._bbox2

    @property
    def arc1(self):
        return self._arc1

    @property
    def arc2(self):
        return self._arc2
    
    def translate(self, translate : Point):
        return Arc(self._bbox1 + translate, self._bbox2 + translate, self._arc1 + translate, self._arc2 + translate)
    
    def rotate(self, degrees):
        return Arc(self._bbox1.rotate(degrees), self._bbox2.rotate(degrees), self._arc1.rotate(degrees), self._arc2.rotate(degrees))
    
    def __str__(self):
        return f"Arc(bb1={self._bbox1}, bb2={self._bbox2}, a1={self._arc1}, a2={self._arc2})"



#######################################################################################################################
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
    
    def translate(self, translate : Point):
        return Line(self._p1 + translate, self._p2 + translate)
    
    def rotate(self, degrees):
        return Line(self._p1.rotate(degrees), self._p2.rotate(degrees))



#######################################################################################################################
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



#######################################################################################################################
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
    
    def translate(self, translate : Point):
        return Rectangle(self._p + translate, self._w, self._h)
    
    def rotate(self, degrees):
        # TODO - This won't work for rotations other than 90 degrees. Fortunately LTSpice only does 90, 180, etc
        if degrees == 0:
            return self
        elif degrees == 90 or degrees == 270:
            return Rectangle(self._p.rotate(degrees), self._h, self._w)
        elif degrees == 180:
            return Rectangle(self._p.rotate(degrees), self._w, self._h)
        else:
            raise Exception(f"Rotation of {degrees} is not supported for Rectangle")


#######################################################################################################################
class Ellipse:
    def __init__(self, cx, cy, w, h):
        self._cx = cx
        self._cy = cy
        self._h = h
        self._w = w
    
    @property 
    def cx(self):
        return self._cx
    
    @property 
    def cy(self):
        return self._cy
    
    @property 
    def h(self):
        return self._h

    @property 
    def w(self):
        return self._w



#######################################################################################################################
class Component:
    def __init__(self, filename):
        self._lines = []
        self._pins  = []
        self._rectangles = []
        self._arcs = []
        self._ellipses = []
        self._windows = []
        arc_index = 0
        state = "idle"
        curret_pin = None

        with open(filename, "r") as fh:
            filecontents = fh.readlines()
            for line in filecontents:
                line =  line.strip()

                while True:
                    if state == "idle":
                        if line[0:len("LINE ")] == "LINE ":
                            line = line.split()[1:]
                            print("LINE", line)
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
                            self._rectangles.append(Rectangle(Point(x1, y1), x2 - x1, y2 - y1))

                        elif line[0:len("ARC ")] == "ARC ":
                            line = line.split()[1:]
                            if not represents_int(line[0]):
                                line = line[1:]

                            bbox_x1 = float(line[0])
                            bbox_y1 = float(line[1])
                            bbox_x2 = float(line[2])
                            bbox_y2 = float(line[3])
                            arc1x   = float(line[4])
                            arc1y   = float(line[5])
                            arc2x   = float(line[6])
                            arc2y   = float(line[7])
                            arc_index += 1

                            self._arcs.append((
                                    LTArc(
                                        LTPoint(bbox_x1, bbox_y1),
                                        LTPoint(bbox_x2, bbox_y2),
                                        LTPoint(arc1x, arc1y),
                                        LTPoint(arc2x, arc2y)
                                    ),
                                    arc_index))

                        elif line[0:len("CIRCLE ")] == "CIRCLE ":
                            line = line.split()[1:]
                            if not represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            cx = min(x1, x2) + abs(x1 - x2)/2
                            cy = min(y1, y2) + abs(y1 - y2)/2
                            w = abs(x1 - x2)
                            h = abs(y1 - y2)
                            self._ellipses.append(Ellipse(cx, cy, w, h))
                        
                        elif line[0:len("WINDOW ")] == "WINDOW ":
                            line = line.split()[1:]
                            a = float(line[0])
                            b = float(line[1])
                            c = float(line[2])
                            d = line[3]
                            e = float(line[4])
                            self._windows.append((a,b,c,d,e))
                            

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
    
    @property
    def ellipses(self):
        return self._ellipses
    
def radians_to_degrees(radians):
    return radians * 180 / math.pi

def draw_ltspice_arc(ax, arc : LTArc, idx, debug=True):
    arc_centered_at_origin = arc.translate(-arc.bbox.center)
    # LTSpice coordinates are like a screen, but atan2 expects them to be like a graph. This means when looking at
    # an LTSpice arc, what I think of as the 1st quadrant is really the 4th, what I think of as the 2nd is the
    # 3rd, what I think of as the 3rd is the 2nd and what I think of a the 4th is the 1st. Which is just the mirror
    # in the y-axis because LTSpice coordinates are screen coordinates and atan is graph coordinates.
    #
    # If I give atan the screen coordinates they are the wrong way around because everything is flipped about the
    # yaxis so swap em! 
    t2      = radians_to_degrees(math.atan2(arc_centered_at_origin.p1.y, arc_centered_at_origin.p1.x))
    t1      = radians_to_degrees(math.atan2(arc_centered_at_origin.p2.y, arc_centered_at_origin.p2.x))
    
    if debug:
        print(f"{idx})\n\tarc    = {arc},\n\tarc_00 = {arc_centered_at_origin},\n\tt1     = {t1},\n\tt2     = {t2}")
        ax.text(*arc.bbox.center.as_tuple(), f"{idx}", color="r")
        ax.add_patch(mpatches.Circle(arc.bbox._topleft.as_tuple(), 1, color='orange'))
        ax.add_patch(mpatches.Circle(arc.bbox._bottomright.as_tuple(), 1, color='blue'))

        # Another interesting facet is that the points p1, p2 need not be at the exact point of the
        # arc start or finish, but can be anywhere on the line from the center to the point. This is
        # just interesting, doesn't effect any calculations...
        ax.add_patch(mpatches.Circle(arc.p1.as_tuple(), 0.5, color='r'))
        ax.text(*arc.p1.as_tuple(), f"p1", color="r")
        ax.add_patch(mpatches.Circle(arc.p2.as_tuple(), 0.5, color='g'))
        ax.text(*arc.p2.as_tuple(), f"p2", color="r")
        ax.add_patch(mpatches.Circle(arc.bbox.center.as_tuple(),    1, color='purple'))
        ax.add_patch(mpatches.Rectangle(arc.bbox._topleft.as_tuple(), *arc.bbox.dimensions.as_tuple(), color='green', fill=False))

    ax.add_patch(
        mpatches.Arc(
            arc.bbox.center.as_tuple(), *arc.bbox.dimensions.as_tuple(), angle=0, theta1=t1, theta2=t2, color='b'))


# bbox_x1, bbox_y1, bbox_x2, bbox_y2, arc1x, arc1y, arc2x, arc2y
def draw_ltspice_arc2(ax, arc, idx):
    """
    This is an ugly mess - plots the arcs correctly but I need to go over it again to properly figure it out, especially to get the bounding box correctly calculated
    """
    arc1x = arc.arc1.x
    arc1y = arc.arc1.y
    arc2x = arc.arc2.x
    arc2y = arc.arc2.y

    bbox_x1 = arc.bbox1.x
    bbox_y1 = arc.bbox1.y
    bbox_x2 = arc.bbox2.x
    bbox_y2 = arc.bbox2.y
    bbox_w = bbox_x2 - bbox_x1
    bbox_h = bbox_y2 - bbox_y1


    # Make the top left of the arc's bounding box the minumum coordinates so that the width and heigh are positive.
    if bbox_w < 0:
        bbox_w = -bbox_w
        t = bbox_x1 
        bbox_x1 = bbox_x2
        bbox_x2 = t
    
    
    if bbox_h < 0:
        bbox_h = -bbox_h
        t = bbox_y1 
        bbox_y1 = bbox_y2
        bbox_y2 = t


    # Get the center of the arc's bounding box
    bbox_xc = bbox_x1 + bbox_w / 2
    bbox_yc = bbox_y1 + bbox_h / 2

    ax.text(bbox_xc, bbox_yc, f"{idx}", color="r")
    ax.add_patch(mpatches.Circle((arc1x, arc1y), 1, color='r'))
    ax.add_patch(mpatches.Circle((arc2x, arc2y), 1, color='g'))
    ax.add_patch(mpatches.Circle((bbox_xc, bbox_yc), 1, color='purple'))
    ax.add_patch(mpatches.Rectangle((bbox_x1, bbox_y1), bbox_w, bbox_h, color='green', fill=False))

    # Need to shift the center to 0 and the coordinates relative to the center at 0.
    # So...
    arc1x_2 = arc1x - bbox_xc
    arc1y_2 = arc1y - bbox_yc
    arc2x_2 = arc2x - bbox_xc
    arc2y_2 = arc2y - bbox_yc

    ret = (min(arc1x, arc2x), min(arc1y, arc2y), max(arc1x, arc2x), max(arc1y, arc2y))

    t1 = math.atan2(arc1y_2, arc1x_2) * 180 / math.pi #< degrees
    t2 = math.atan2(arc2y_2, arc2x_2) * 180 / math.pi #< degrees
    

    if (t1 >= 0 and t2 < 0) or (t2 >= 0 and t1 < 0) or (t1 > t2):
        # MPL wants to draw anti-clockwise from t1 to t2, where as it would seem LTSpice draws clockwise.
        # In these cases it would draw the wrong part of the arc because it would need to go CW from t1 to t2.
        # So, by swapping t1 and t2 it will draw it correctly.
        ret = (min(bbox_x1, bbox_x2), min(bbox_y1, bbox_y2), max(bbox_x1, bbox_x2), max(bbox_y1, bbox_y2))
        t = t1
        t1 = t2
        t2 = t
        print(f"ARC {idx} p1=({arc1x_2}, {arc1y_2}), p2=({arc2x_2}, {arc2y_2}), t1={t1}, t2={t2} (swapped)")
    else:
        print(f"ARC {idx} p1=({arc1x_2}, {arc1y_2}), p2=({arc2x_2}, {arc2y_2}), t1={t1}, t2={t2}")

    arc1 = mpatches.Arc((bbox_xc, bbox_yc), bbox_w, bbox_h, angle=0, theta1=t1, theta2=t2, color='b')
    ax.add_patch(arc1)

    return ret




def update_minx(x1,x2):
    global minx
    thismin = min(x1,x2)
    if thismin < minx:
        minx = thismin

def update_maxx(x1,x2):
    global maxx
    thismax = max(x1,x2)
    if thismax > maxx:
        maxx = thismax


def update_miny(y1,y2):
    global miny
    thismin = min(y1,y2)
    if thismin < miny:
        miny = thismin


def update_maxy(y1,y2):
    global maxy
    thismax = max(y1,y2)
    if thismax > maxy:
        maxy = thismax


def update_minmax(x1, y1, x2, y2):
    update_minx(x1, x2)
    update_maxx(x1, x2)
    update_miny(y1, y2)
    update_maxy(y1, y2)


def matplotlib_plot_component(component, ax, xoff = 0, yoff = 0, rotation = 0):
    global minx, miny, maxx, maxy
    minx = 1000000.0
    miny = 1000000.0
    maxx = -1000000.0
    maxy = -1000000.0
    
    print("PLOTTING")

    for line in component.lines:
        print("LINE MINMAX")
        update_minmax(line.p1.x, line.p1.y, line.p2.x, line.p2.y)

    for rect in component.rectangles:
        update_minmax(rect.p.x, rect.p.y, rect.p.x + rect.w, rect.p.y + rect.h)

    for ellipse in component.ellipses:
        update_minmax(ellipse.cx - ellipse.w/2, ellipse.cy - ellipse.h/2, ellipse.cx + ellipse.w/2, ellipse.cy + ellipse.h/2)

    #for arc, arc_index in component.arcs:
    #    update_minmax(arc.bbox.x, arc.bbox.y, arc.bbox2.x, arc.bbox2.y)


    mwidth = maxx-minx
    mheight = maxy-miny

    print(minx, miny)
    print(maxx, maxy)
    print(mwidth, mheight)

    for line in component.lines:
        line = line.translate(Point(-minx, -miny)).rotate(rotation).translate(Point(minx, miny))
        ax.plot([line.p1.x + xoff, line.p2.x + xoff], [line.p1.y + yoff, line.p2.y + yoff], color='b')

    for rect in component.rectangles:
        rect = rect.translate(Point(-minx, -miny)).rotate(rotation).translate(Point(minx, miny))
        rect1 = mpatches.Rectangle((rect.p.x + xoff, rect.p.y + yoff), rect.w, rect.h, fill=False, color='b')
        ax.add_patch(rect1)

    for ellipse in component.ellipses:
        el1 = mpatches.Ellipse((ellipse.cx + xoff, ellipse.cy + yoff), ellipse.w, ellipse.h, fill=False, color='b')
        ax.add_patch(el1)

    #for pin in component.pins:
    #    circle1 = mpatches.Circle((pin.p.x + xoff, pin.p.y + yoff), 1, color='r')
    #    ax.add_patch(circle1)
    #    if pin.name is not None:
    #        ax.text(pin.p.x, pin.p.y, pin.name)

    for arc, arc_index in component.arcs[0:]:
        r = draw_ltspice_arc(ax, arc.translate(LTPoint(xoff, yoff)), arc_index)




if __name__ == "__main__":
    import tempfile
    import os
    import fnmatch

    def YieldFiles(dirToScan, mask):
        for rootDir, subDirs, files in os.walk(dirToScan):
            for fname in files:
                if fnmatch.fnmatch(fname, mask):
                    yield (rootDir, fname)

    #for dir, file in YieldFiles("/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym", "*.asy"):
    #for dir, file in YieldFiles("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator", "arc_quad1_type1bbox_t1_gt_t2.asy"):
    for dir, file in YieldFiles("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator", "*.asy"):
        try:
            fn = os.path.join(dir, file)
            print(fn)
            with open(fn, "r") as fh:
                print("\n".join(fh.readlines()))
            fig, ax = pl.subplots()
            #ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
            #ax.set_xticks([]) 
            #ax.set_yticks([]) 
            matplotlib_plot_component(Component(fn), ax)
            MARGIN = 5
            #ax.set_xlim(minx - MARGIN, maxx + MARGIN)
            #ax.set_ylim(miny - MARGIN, maxy + MARGIN)
            ax.set_xlim(-50,50)
            ax.set_ylim(-50,50)
            ax.invert_yaxis()
            fig.tight_layout()
            fig.show()
            pl.show()
            pl.close(fig)
        except Exception as e:
            print(e)
            raise
