"""
Copyright 2024 James E Hume

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import math
from lt_shapes import LTPoint, LTRectangle, LTArc, LTLine, LTEllipse, LTPin
from lt_component import LTComponent
from minmax import MinMax


#######################################################################################################################
def radians_to_degrees(radians):
    return radians * 180 / math.pi


#######################################################################################################################
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


#######################################################################################################################
def rotate_quadrants(quad):
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
    

#######################################################################################################################
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

    t2_quad = rotate_quadrants(get_quadrant_1_to_4(t1_degs))
    t1_quad = rotate_quadrants(get_quadrant_1_to_4(t2_degs))
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



#######################################################################################################################
def matplotlib_plot_component(
        component   : LTComponent,
        ax          : pl.Axes,
        xoff        : int  = 0,
        yoff        : int  = 0,
        rotation    : int  = 0,
        show_labels : bool = False,
        debug       : bool = False):

    component.rotate(rotation)
    component.translate(LTPoint(xoff, yoff))

    # Now draw the component
    for line in component.lines:
        ax.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color='b')

    for rect in component.rectangles:
        ax.add_patch(
            mpatches.Rectangle(rect.topleft.as_tuple(), *rect.dimensions.as_tuple(), fill=False, color='b'))

    for ellipse in component.ellipses:
        ax.add_patch(
            mpatches.Ellipse(ellipse.xy.as_tuple(), ellipse.w, ellipse.h, fill=False, color='b'))

    for pin in component.pins:
        ax.add_patch(mpatches.Circle(pin.p.as_tuple(), 1, color='r'))
        if show_labels and pin.name is not None:
            ax.text(pin.p.x, pin.p.y, pin.name)

    for arc, arc_index in component.arcs:
        draw_ltspice_arc(ax, arc, arc_index, draw=True, debug=False)

    return component.minmax


if __name__ == "__main__":
    import tempfile
    import os
    import fnmatch
    from itertools import chain

    def YieldFiles(dirToScan, mask):
        for rootDir, subDirs, files in os.walk(dirToScan):
            for fname in files:
                if fnmatch.fnmatch(fname, mask):
                    yield (rootDir, fname)

    asy_file_iter = chain.from_iterable([
        YieldFiles("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator", "*.asy"),
        YieldFiles("/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym", "*.asy"),
    ])

    for dir, file in asy_file_iter:
        try:
            fn = os.path.join(dir, file)
            fig, ax = pl.subplots()
            ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
            ax.set_xticks([]) 
            ax.set_yticks([]) 
            minmax = matplotlib_plot_component(LTComponent(fn), ax)
            MARGIN = 5
            ax.set_xlim(minmax.min.x - MARGIN, minmax.max.x + MARGIN)
            ax.set_ylim(minmax.min.y - MARGIN, minmax.max.y + MARGIN)
            ax.invert_yaxis()
            ax.set_title(os.path.join(dir, file))
            fig.tight_layout()
            fig.show()
            pl.show()
            pl.close(fig)
        except Exception as e:
            print(e)
            raise
