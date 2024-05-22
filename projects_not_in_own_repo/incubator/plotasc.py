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

        with open(filename, "r", encoding="utf-8", errors="ignore") as fh:
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

def get_quadrant_1_to_4(degrees):
    if degrees >= 0:
        if degrees <= 90:
            return 1
        elif degrees <= 180:
            return 2
        elif degrees <= 270:
            return 3
        elif degrees <= 360:
            return 4
    else:
        if degrees <= -270:
            return 1
        elif degrees <= -180:
            return 2
        elif degrees <= -90:
            return 3
        else:
            return 4
        
    raise RuntimeError(f"get_quadrant_1_to_4({degrees}) not supported")

def maybe(quad):
    # LTSpice coordinates are like a screen, but atan2 expects them to be like a graph. This means when looking at
    # an LTSpice arc, what I think of as the 1st quadrant is really the 4th, what I think of as the 2nd is the
    # 3rd, what I think of as the 3rd is the 2nd and what I think of a the 4th is the 1st. 
    if quad == 1:
        return 4
    if quad == 2:
        return 3
    if quad == 3:
        return 2
    
    return 1
    
def draw_ltspice_arc(ax, arc : LTArc, idx, debug=True):
    print("\n\n\n\n\nPlotting ARC IDX", idx)
    arc_centered_at_origin = arc.translate(-arc.bbox.center)

    # LTSpice coordinates are like a screen, but atan2 expects them to be like a graph. This means when looking at
    # an LTSpice arc, what I think of as the 1st quadrant is really the 4th, what I think of as the 2nd is the
    # 3rd, what I think of as the 3rd is the 2nd and what I think of a the 4th is the 1st. Which is just the mirror
    # in the y-axis because LTSpice coordinates are screen coordinates and atan is graph coordinates.
    #
    # If I give atan the screen coordinates they are the wrong way around because everything is flipped about the
    # yaxis so swap em! 
    t1_rads = math.atan2(arc_centered_at_origin.p2.y, arc_centered_at_origin.p2.x)
    t2_rads = math.atan2(arc_centered_at_origin.p1.y, arc_centered_at_origin.p1.x)

    t1_degs = radians_to_degrees(t1_rads)
    t2_degs = radians_to_degrees(t2_rads)

    if t1_degs < 0 : t1_degs += 360.0
    if t2_degs < 0 : t2_degs += 360.0

    arc_radii = arc.bbox.dimensions / 2
    
    # Another interesting facet is that the points p1, p2 need not be at the exact point of the arc start or finish,
    # but can be anywhere on the line from the center to the point. Thus, calculate the "real" points...
    # Because t1 and t2 are swapped above, swap them back for get the right point index
    arc_real_p2 = LTPoint(arc_radii.x * math.cos(t1_rads), arc_radii.y * math.sin(t1_rads)).translate(arc.bbox.center)
    arc_real_p1 = LTPoint(arc_radii.x * math.cos(t2_rads), arc_radii.y * math.sin(t2_rads)).translate(arc.bbox.center)

    t2_quad = maybe(get_quadrant_1_to_4(t1_degs))
    t1_quad = maybe(get_quadrant_1_to_4(t2_degs))
    print("QUAD1", t1_quad, "from", t1_degs)
    print("QUAD2", t2_quad, "from", t2_degs)

    if t1_degs < t2_degs:
        # The arc is going AC and is the short arc between the two points
        print("The arc is going AC and is the short arc between the two points")
        quads = sorted(list(range(t1_quad, t2_quad + 1)))

    else:
        # The arc is going AC and is the long arc between the two points
        print("The arc is going AC and is the long arc between the two points")
        tmp = list(range(t1_quad, 5))
        tmp.extend(list(range(1, t2_quad + 1)))
        quads = sorted(tmp)

    print("QUADS", quads)

    tight_bbox = arc.bbox.clone()
  
    if 1 in quads and 2 in quads:
        tight_bbox.topleft.y = arc.bbox.topleft.y
    else:
        print("MINY")
        tight_bbox.topleft.y = min(arc_real_p1.y, arc_real_p2.y)
    
    if 2 in quads and 3 in quads:
        tight_bbox.topleft.x = arc.bbox.topleft.x
    else:
        print("MINX")
        tight_bbox.topleft.x = min(arc_real_p1.x, arc_real_p2.x)
    
    if 3 in quads and 4 in quads:
        tight_bbox.bottomright.y = arc.bbox.bottomright.y
    else:
        print(f"MAXY = max({arc.p1.y}, {arc.p2.y})")
        tight_bbox.bottomright.y = max(arc_real_p1.y, arc_real_p2.y)
    
    if 4 in quads and 1 in quads:        
        tight_bbox.bottomright.x = arc.bbox.bottomright.x
    else:
        print(f"MAXX = max({arc.p1.x}, {arc.p2.x}) ")
        tight_bbox.bottomright.x = max(arc_real_p1.x, arc_real_p2.x)

    if len(quads) == 4 and t1_quad != t2_quad:
        # The edge between the two points might be shrinkable
        quads = [t1_quad, t2_quad]
        if 1 in quads and 2 in quads:
            tight_bbox.topleft.y = min(arc_real_p1.y, arc_real_p2.y)
        if 2 in quads and 3 in quads:
            tight_bbox.topleft.x = min(arc_real_p1.x, arc_real_p2.x)
        if 3 in quads and 4 in quads:
            tight_bbox.bottomright.y = max(arc_real_p1.y, arc_real_p2.y)
        if 4 in quads and 1 in quads:
            tight_bbox.bottomright.x = max(arc_real_p1.x, arc_real_p2.x)


    print(f"tight_bbox={tight_bbox}")
    
    if debug:
        print(f"{idx})\n\tarc    = {arc},\n\tarc_00 = {arc_centered_at_origin},\n\tt1     = {t1_degs},\n\tt2     = {t2_degs}")
        ax.text(*arc.bbox.center.as_tuple(), f"{idx}", color="r")
        ax.add_patch(mpatches.Circle(arc.bbox._topleft.as_tuple(), 1, color='orange'))
        ax.add_patch(mpatches.Circle(arc.bbox._bottomright.as_tuple(), 1, color='blue'))
        ax.add_patch(mpatches.Rectangle(tight_bbox._topleft.as_tuple(), *tight_bbox.dimensions.as_tuple(), color='yellow', fill=False))       
        ax.add_patch(mpatches.Circle(arc_real_p1.as_tuple(), 0.5, color='r'))
        ax.add_patch(mpatches.Circle(arc_real_p2.as_tuple(), 0.5, color='g'))
        ax.text(*arc_real_p1.as_tuple(), f"p1", color="r")
        ax.text(*arc_real_p2.as_tuple(), f"p2", color="g")

        
        ax.add_patch(mpatches.Circle(arc.bbox.center.as_tuple(),    1, color='purple'))
        ax.add_patch(mpatches.Rectangle(arc.bbox._topleft.as_tuple(), *arc.bbox.dimensions.as_tuple(), color='green', fill=False))

    ax.add_patch(
        mpatches.Arc(
            arc.bbox.center.as_tuple(), *arc.bbox.dimensions.as_tuple(), angle=0, theta1=t1_degs, theta2=t2_degs, color='b'))

    return tight_bbox



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

    for pin in component.pins:
        circle1 = mpatches.Circle((pin.p.x + xoff, pin.p.y + yoff), 1, color='r')
        ax.add_patch(circle1)
        if pin.name is not None:
            ax.text(pin.p.x, pin.p.y, pin.name)

    for arc, arc_index in component.arcs[0:]:
        tight_bbox = draw_ltspice_arc(ax, arc.translate(LTPoint(xoff, yoff)), arc_index, debug=False)
        update_minmax(tight_bbox.topleft.x, tight_bbox.topleft.y, tight_bbox.bottomright.x, tight_bbox.bottomright.y)




if __name__ == "__main__":
    import tempfile
    import os
    import fnmatch

    def YieldFiles(dirToScan, mask):
        for rootDir, subDirs, files in os.walk(dirToScan):
            for fname in files:
                if fnmatch.fnmatch(fname, mask):
                    yield (rootDir, fname)

    for dir, file in YieldFiles("/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym", "*.asy"):
    #for dir, file in YieldFiles("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator", "arc_quad1_type2bbox_assorted.asy"):
    #for dir, file in YieldFiles("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator", "*.asy"):
        try:
            fn = os.path.join(dir, file)
            print(fn)
            with open(fn, "r", encoding="utf-8", errors="ignore") as fh:
                print("\n".join(fh.readlines()))
            fig, ax = pl.subplots()
            ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
            ax.set_xticks([]) 
            ax.set_yticks([]) 
            matplotlib_plot_component(Component(fn), ax)
            MARGIN = 5
            ax.set_xlim(minx - MARGIN, maxx + MARGIN)
            ax.set_ylim(miny - MARGIN, maxy + MARGIN)
            ax.invert_yaxis()
            fig.tight_layout()
            fig.show()
            pl.show()
            pl.close(fig)
        except Exception as e:
            print(e)
            raise
