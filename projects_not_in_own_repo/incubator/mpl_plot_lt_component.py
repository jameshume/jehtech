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
def draw_ltspice_arc(ax, arc : LTArc, idx, debug=True):
    print(f"DRAW ARC {arc}")
    ax.add_patch(
        mpatches.Arc(
            arc.bbox.center.as_tuple(), *arc.bbox.dimensions.as_tuple(), angle=0, theta1=arc.t1_degs, theta2=arc.t2_degs, color='b', linewidth=pl.rcParams['lines.linewidth']))




#######################################################################################################################
def matplotlib_plot_component(
        component   : LTComponent,
        ax          : pl.Axes,
        show_labels : bool = False):

    # Now draw the component
    for line in component.lines:
        ax.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color='b')

    for rect in component.rectangles:
        ax.add_patch(
            mpatches.Rectangle(rect.topleft.as_tuple(), *rect.dimensions.as_tuple(), fill=False, color='b', linewidth=pl.rcParams['lines.linewidth']))

    for ellipse in component.ellipses:
        ax.add_patch(
            mpatches.Ellipse(ellipse.xy.as_tuple(), ellipse.w, ellipse.h, fill=False, color='b', linewidth=pl.rcParams['lines.linewidth']))

    for pin in component.pins:
        ax.add_patch(mpatches.Circle(pin.p.as_tuple(), 1, color='r', linewidth=pl.rcParams['lines.linewidth']))
        if show_labels and pin.name is not None:
            ax.text(pin.p.x, pin.p.y, pin.name)

    for arc, arc_index in component.arcs:
        draw_ltspice_arc(ax, arc, arc_index, debug=False)

    ax.text( 
        component.minmax.max.x + (component.minmax.max.x - component.minmax.min.x) *.05, 
        component.minmax.min.y + (component.minmax.max.y - component.minmax.min.y) / 2, 
        component.name)

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
