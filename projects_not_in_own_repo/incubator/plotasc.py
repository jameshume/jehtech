import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import math
from shapes import LTPoint, LTRectangle, LTArc, LTLine, LTEllipse, LTPin


#######################################################################################################################
def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True



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
        print ("MAKING COMPONENT")

        with open(filename, "r", encoding="utf-8", errors="ignore") as fh:
            filecontents = fh.readlines()
            for line in filecontents:
                line = line.strip()

                while True:
                    print(">>>>", line)
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
                                LTLine(
                                    LTPoint(x1, y1),
                                    LTPoint(x2, y2)
                                )
                            )

                        elif line[0:len("PIN ")] == "PIN ":
                            line = line.split()[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            curret_pin = LTPin(x1, y1)
                            state = "pin"
#
                        elif line[0:len("RECTANGLE ")] == "RECTANGLE ":
                            line = line.split()[1:]
                            if not represents_int(line[0]):
                                line = line[1:]
                            x1 = float(line[0])
                            y1 = float(line[1])
                            x2 = float(line[2])
                            y2 = float(line[3])
                            self._rectangles.append(LTRectangle(LTPoint(x1, y1), LTPoint(x2, y2)))

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
                            self._ellipses.append(LTEllipse(LTPoint(cx, cy), w, h))
                        
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
                                self._pins.append(LTPin(LTPoint(x1, y1), line[1]))
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
    
    @property
    def flags(self):
        return self._flags


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
    
def draw_ltspice_arc(ax, arc : LTArc, idx, draw=True, debug=True):
    if debug:
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
    if debug:
        print("QUAD1", t1_quad, "from", t1_degs)
        print("QUAD2", t2_quad, "from", t2_degs)

    if t1_degs < t2_degs:
        # The arc is going AC and is the short arc between the two points
        if debug:
            print("The arc is going AC and is the short arc between the two points")
        quads = sorted(list(range(t1_quad, t2_quad + 1)))

    else:
        # The arc is going AC and is the long arc between the two points
        if debug: 
            print("The arc is going AC and is the long arc between the two points")
        tmp = list(range(t1_quad, 5))
        tmp.extend(list(range(1, t2_quad + 1)))
        quads = sorted(tmp)

    if debug:
        print("QUADS", quads)

    tight_bbox = arc.bbox.clone()
  
    if 1 in quads and 2 in quads:
        tight_bbox.topleft.y = arc.bbox.topleft.y
    else:
        tight_bbox.topleft.y = min(arc_real_p1.y, arc_real_p2.y)
    
    if 2 in quads and 3 in quads:
        tight_bbox.topleft.x = arc.bbox.topleft.x
    else:
        tight_bbox.topleft.x = min(arc_real_p1.x, arc_real_p2.x)
    
    if 3 in quads and 4 in quads:
        tight_bbox.bottomright.y = arc.bbox.bottomright.y
    else:
        tight_bbox.bottomright.y = max(arc_real_p1.y, arc_real_p2.y)
    
    if 4 in quads and 1 in quads:        
        tight_bbox.bottomright.x = arc.bbox.bottomright.x
    else:
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


    if debug:
        print(f"tight_bbox={tight_bbox}")
    
    if draw:
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


def matplotlib_plot_component(component, ax, xoff = 0, yoff = 0, rotation = 0, show_labels=False, debug=False):
    global minx, miny, maxx, maxy
    minx = 1000000.0
    miny = 1000000.0
    maxx = -1000000.0
    maxy = -1000000.0
    
    for line in component.lines:
        update_minmax(line.p1.x, line.p1.y, line.p2.x, line.p2.y)

    for rect in component.rectangles:
        update_minmax(*rect.topleft.as_tuple(), *rect.bottomright.as_tuple())

    for ellipse in component.ellipses:
        update_minmax(ellipse.xy.x - ellipse.w/2, 
                      ellipse.xy.y - ellipse.h/2, 
                      ellipse.xy.x + ellipse.w/2, 
                      ellipse.xy.y + ellipse.h/2)

    for arc, arc_index in component.arcs[0:]:
        tight_bbox = draw_ltspice_arc(ax, arc, arc_index, draw=False, debug=False)
        update_minmax(tight_bbox.topleft.x, tight_bbox.topleft.y, tight_bbox.bottomright.x, tight_bbox.bottomright.y)

    for line in component.lines:
        line = line.rotate(rotation)
        line = line.translate(LTPoint(xoff, yoff))
        ax.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color='b')

    for rect in component.rectangles:
        rect = rect.rotate(rotation)
        rect = rect.translate(LTPoint(xoff, yoff))
        rect1 = mpatches.Rectangle(rect.topleft.as_tuple(), *rect.dimensions.as_tuple(), fill=False, color='b')
        ax.add_patch(rect1)

    for ellipse in component.ellipses:
        ellipse = ellipse.rotate(rotation)
        ellipse = ellipse.translate(LTPoint(xoff, yoff))
        el1 = mpatches.Ellipse(ellipse.xy.as_tuple(), ellipse.w, ellipse.h, fill=False, color='b')
        ax.add_patch(el1)

    for pin in component.pins:
        pin = pin.rotate(rotation)
        pin = pin.translate(LTPoint(xoff, yoff))

        circle1 = mpatches.Circle(pin.p.as_tuple(), 1, color='r')
        ax.add_patch(circle1)
        if show_labels and pin.name is not None:
            ax.text(pin.p.x, pin.p.y, pin.name)

    for arc, arc_index in component.arcs:
        arc = arc.rotate(rotation)
        arc = arc.translate(LTPoint(xoff, yoff))
        draw_ltspice_arc(ax, arc, arc_index, draw=True, debug=False)

    if debug:
        rect_minmax = LTRectangle(LTPoint(minx, miny), LTPoint(maxx, maxy)).rotate(rotation).translate(LTPoint(xoff, yoff))
        rect_patch = mpatches.Rectangle(rect_minmax.topleft.as_tuple(), *rect_minmax.dimensions.as_tuple(), fill=False, color='orange')
        ax.add_patch(rect_patch)



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
            ax.set_title(os.path.join(dir, file))
            fig.tight_layout()
            fig.show()
            pl.show()
            pl.close(fig)
        except Exception as e:
            print(e)
            raise
