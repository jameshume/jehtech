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
    mplarc = mpatches.Arc(
            arc.bbox.center.as_tuple(), 
            *arc.bbox.dimensions.as_tuple(), 
            angle=0, 
            theta1=arc.t1_degs, 
            theta2=arc.t2_degs, 
            color='b', 
            linewidth=pl.rcParams['lines.linewidth'])
    ax.add_patch(mplarc)
    return mplarc


class MPL_LTComponent(LTComponent):
    def __init__(self, totalname, name):
        super().__init__(totalname, name)
        self._mpllines      : list[pl.Line2D]      = []
        self._mplrectangles : list[mpatches.Patch] = []
        self._mplellipses   : list[mpatches.Patch] = []
        self._mplpins       : list[mpatches.Patch] = []
        self._mplpin_labels : list[pl.Text]        = []
        self._mplarcs       : list[mpatches.Patch] = []
        self._mplname       : pl.Text              = None
    
    def set_colour(self, colour):
        for line in self._mpllines:
            line.set_color(colour)
        for rect in self._mplrectangles:
            rect.set_edgecolor(colour)
        for ellipse in self._mplellipses:
            ellipse.set_edgecolor(colour)
        for pin in self._mplpins:
            pin.set_edgecolor(colour)
        for arc in self._mplarcs:
            arc.set_colour(colour)
        

    def add_line(self, line):
        self._mpllines.append(line)

    def add_rectangle(self, rect):
        self._mplrectangles.append(rect)
    
    def add_ellipse(self, ellipse):
        self._mplellipses.append(ellipse)

    def add_pin(self, pin):
        self._mplpins.append(pin)
    
    def add_pin_label(self, label):
        self._mplpin_labels.append(label)

    def add_arc(self, arc):
        self._mplarcs.append(arc)
    
    def add_name_text(self, name):
        self._mplname = name

    def get_minmax(self):
        return self.minmax




#######################################################################################################################
def matplotlib_plot_component(
        totalname, name, rotation, x, y,
        ax          : pl.Axes,
        show_labels : bool = False):
    
    mpl_component = MPL_LTComponent(totalname, name)
    mpl_component.rotate(rotation)
    mpl_component.translate(LTPoint(x, y))

    # Now draw the component
    for line in mpl_component.lines:
        mplline, = ax.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color='b')
        mpl_component.add_line(mplline)

    for rect in mpl_component.rectangles:
        mplpatch = ax.add_patch(
            mpatches.Rectangle(
                rect.topleft.as_tuple(), 
                *rect.dimensions.as_tuple(), 
                fill=False, 
                color='b', 
                linewidth=pl.rcParams['lines.linewidth']))
        mpl_component.add_rectangle(mplpatch)

    for ellipse in mpl_component.ellipses:
        mplpatch = ax.add_patch(
            mpatches.Ellipse(
                ellipse.xy.as_tuple(), 
                ellipse.w, 
                ellipse.h, 
                fill=False, 
                color='b', 
                linewidth=pl.rcParams['lines.linewidth']))
        mpl_component.add_ellipse(mplpatch)

    for pin in mpl_component.pins:
        mplpatch = ax.add_patch(
            mpatches.Circle(pin.p.as_tuple(), 1, color='r', linewidth=pl.rcParams['lines.linewidth']))
        mpl_component.add_pin(mplpatch)
        if show_labels and pin.name is not None:
            mplpatch = ax.text(pin.p.x, pin.p.y, pin.name)
            mpl_component.add_pin_label(mplpatch)

    for arc, arc_index in mpl_component.arcs:
        mplarc = draw_ltspice_arc(ax, arc, arc_index, debug=False)
        mpl_component.add_arc(mplarc)


    mplname = ax.text( 
        mpl_component.minmax.max.x + (mpl_component.minmax.max.x - mpl_component.minmax.min.x) *.05, 
        mpl_component.minmax.min.y + (mpl_component.minmax.max.y - mpl_component.minmax.min.y) / 2, 
        mpl_component.name)
    mpl_component.add_name_text(mplname)

    return mpl_component


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
            mpl_ltcomponent = matplotlib_plot_component(LTComponent(fn), ax)
            minmax = mpl_ltcomponent.get_minmax()
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
