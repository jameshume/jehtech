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

"""
Install LTSpice on Linux using Wine:

    sudo dpkg --add-architecture i386
    sudo apt update
    sudo apt install wine64 wine32 winetricks \
                    x11-utils x11-xserver-utils xauth xvfb \
                    libwine libwine:i386

Install LTSpie:
    wget https://ltspice.analog.com/software/LTspice64.exe -O ~/LTspice64.exe

Run installer:
    wine ~/LTspice64.exe
"""

import matplotlib.pyplot as pl
import matplotlib.patches as mpatches

from mpl_plot_lt_component import matplotlib_plot_component, MinMax
from lt_shapes import LTPoint, LTLine, LTPin
from lt_component import LTComponent
from typing import Union, List
from dataclasses import dataclass
from collections import defaultdict

pl.rcParams['lines.linewidth'] = 2



def parse_flag_line(line, minmax, ax, draw=True):
    print(f"parse_flag_line - {line.strip()}")
    flag_x, flag_y, flag_txt = line.strip().split(" ")[1:]
    flag_x, flag_y = (float(flag_x), float(flag_y))
    
    if draw:
        if flag_txt == "0":
            # Plotting ground here - function badly designed as overloaded to not draw for pins :/
            # Todo - to know the orientation we would need to know the "direction" of the wire or component
            # connected to te ground
            circle1 = mpatches.Circle((flag_x, flag_y), 1, color='r', linewidth=pl.rcParams['lines.linewidth'])
            ax.add_patch(circle1)
            minmax.add(LTPoint(flag_x, flag_y))
            hw = 20
            h = 20
            ax.plot([flag_x - hw, flag_x + hw], [flag_y, flag_y], c='b')
            ax.plot([flag_x - hw, flag_x], [flag_y, flag_y + h], c='b')
            ax.plot([flag_x, flag_x + hw], [flag_y + h, flag_y], c='b')
            minmax.add(LTPoint(flag_x - hw, flag_y))
            minmax.add(LTPoint(flag_x - hw, flag_y))
            minmax.add(LTPoint(flag_x, flag_y + h))
            minmax.add(LTPoint(flag_x + hw, flag_y))
            minmax.add(LTPoint(flag_x, flag_y + h))
            minmax.add(LTPoint(flag_x + hw, flag_y))
        else:
            ax.text(x=flag_x, y=flag_y, s=flag_txt)
    return flag_x, flag_y, flag_txt

class PlottedLTLine(LTLine):
    pass

class MPL_LTLine(PlottedLTLine):
    def __init__(self, fig, ax, mpl_line, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mpl_line = mpl_line
        self._fig = fig
        self._ax = ax

    def set_colour(self, colour):
        self._mpl_line.set_color(colour)

    def __str__(self):
        return f"MPL_LTLine({self._p1}, {self._p2})"
    
    def __repr__(self):
        return self.__str__()

class MPL_IoPin:
    def __init__(self, is_out, lines, text_xy, text_str):
        self._is_out   = is_out
        self._lines    = lines
        self._text_xy  = text_xy
        self._text_str = text_str

    def set_colour(self, colour):
        for line in self._lines:
            line.set_color(colour)

def lt_plot_asc(fig, ax, filename):
    state                     = "normal"
    flag_x, flag_y, flag_type = None, None, None
    prev_line_cache           = None
    first_line                = True
    wires                     = []
    minmax                    = MinMax()
    pins                      = {}

    components = []
    mpl_flag_texts = []


    # Really I should have a .asc file parsed and work from there into a plot!
    # Also the plot could be used to generate a graph - which components are connected to which.
    # But there is the netlist for that.
    print(f"OPENING {filename}")
    for line in open(filename, "r"):
        print(line.strip())

        if (prev_line_cache is not None):
            if line.startswith("IOPIN "):
                print(line.strip())
                x, y, inout = line.strip().split(" ")[1:]
                print(x, y, inout)
                x, y = float(x), float(y)
                h = 20
                warrow = 20
                minmax.add(LTPoint(x, y))
                l1, l2 = None, None
                if inout == "Out":
                    minmax.add(LTPoint(x - warrow, y - h))
                    minmax.add(LTPoint(x - warrow, y + h))
                    l1, = ax.plot([x, x - warrow], [y, y - h], c='b')
                    l2, = ax.plot([x, x - warrow], [y, y + h], c='b')
                elif inout == "In":
                    minmax.add(LTPoint(x + warrow, y - h))
                    minmax.add(LTPoint(x + warrow, y + h))
                    l1, = ax.plot([x, x + warrow], [y, y - h], c='b')
                    l2, = ax.plot([x, x + warrow], [y, y + h], c='b')
                else:
                    print(f"##### IO pin type '{inout}' not supported")

                flag_x, flag_y, flag_text = parse_flag_line(prev_line_cache, minmax, ax, draw=False)
                minmax.add(LTPoint(flag_x, flag_y))
                mpl_flag_text = ax.text(flag_x, flag_y, flag_text, fontsize=10)
                mpl_flag_texts.append(mpl_flag_text)

                pins[flag_text] = MPL_IoPin(inout=="Out", [l1, l2], LTPoint(flag_x, flag_y), flag_text )
            else:
                parse_flag_line(prev_line_cache, minmax, ax)
            
            prev_line_cache = None

        first_line = False
        
        if line.startswith("WIRE "):
            x1, y1, x2, y2 = [float(x) for x in line.strip().split(" ")[1:]]
            mpl_line, = ax.plot([x1, x2], [y1, y2], color='blue')
            wires.append(MPL_LTLine(fig, ax, mpl_line, LTPoint(x1, y1), LTPoint(x2, y2)))
            minmax.add(LTPoint(x1, y1))
            minmax.add(LTPoint(x2, y2))

        # Seems like an IOPIN is always
        #   FLAG x y some-string
        #   IOPIN
        #
        # But ground is just
        #   FLAG x y 0
        # Followed by anything other than IOPIN
        elif line.startswith("FLAG "):
            prev_line_cache = line

        elif line.startswith("SYMBOL "):
            tokens = line.strip().split(" ")[1:]
            name = tokens[0].replace("\\", "/")
            totalname = f"/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/{name}.asy"
            x, y, rotation = float(tokens[1]), float(tokens[2]), float(tokens[3][1:])
        
        elif line.startswith("SYMATTR InstName "):
            # Add a new proprty to component with its name
            name = line[len("SYMATTR InstName "):].strip()
            mpl_ltcomponent = matplotlib_plot_component(totalname, name, rotation, x, y, ax, show_labels=False)
            component_minmax = mpl_ltcomponent.get_minmax()
            components.append(mpl_ltcomponent)
            minmax.merge(component_minmax)

        # TODO
        # Symbol can be follwed by window commands:
        # The WINDOW command just sets the position and alignment of labels in the schematic view.
        # WINDOW <index> <x> <y> <alignment> <flags>
        # Field	Meaning
        # index	Which text label it refers to:
        #   - 0 is the component name (e.g., R1, V1)
        #   - 3 is the value (e.g., 1k, 5V)
        # x, y	The position (offset) of the label relative to the symbol origin
        # alignment	Text alignment: Left, Right, Center
        # flags	Usually 0; can affect visibility or font, but not often used manually

        # Also multiple SYMATTR
        #    SYMATTR InstName
        #    SYMATTR Value

    if prev_line_cache is not None:
        prev_line_cache = None
        parse_flag_line(line, minmax, ax)

    # Put all wires and component points in a dictionary
    points_to_wires = defaultdict(list)
    for wire in wires:
        points_to_wires[wire.p1].append(wire)
        points_to_wires[wire.p2].append(wire)

    points_to_pins = defaultdict(list)
    name_to_component = {}
    for component in components:
        name_to_component[component.name] = component
        for pin in component.pins:
            points_to_pins[pin.p].append(pin)
   
    # When a line has a connection to it, if the connection is in the middle of the line,
    # it is broken into two. This means that lines that intersect do so at the start
    # or finish of the line, never in the "middle" of a line. Thus, connections
    # occur when a line starts/ends where another line starts/ends
    #
    # A really simple approach, if inefficient, is to say, for each line, find all lines
    # that start/finish at either the start or finish of this line. If that line exists
    # puts a "join" blob.
    for point, pointlist in points_to_wires.items():
        if len(pointlist) > 1:
            ax.add_patch(mpatches.Circle(point.as_tuple(), 3, color='darkblue', linewidth=pl.rcParams['lines.linewidth']))

    # Now everything is drawn, get text extends to update the min/max - somehow this still isn't quite right -- some text still goes
    # off the end of the axis :/
    # Note quite right but can't be arsed to figure this out right now...
    fig.canvas.draw() # Draw the plot to ensure text is rendered
    for mpl_flag_text in mpl_flag_texts:
        # Get the data-coordinate extent of the text
        bbox = mpl_flag_text.get_window_extent(renderer=fig.canvas.get_renderer()) # In display coordinates. Need to convert to data coordinates
        display_to_data = ax.transData.inverted() # Transformation matrix display -> data coords
        # Convert the width from display to data coordinates
        data_coords_1 = display_to_data.transform((bbox.x0, bbox.y0))
        data_coords_2 = display_to_data.transform((bbox.x1, bbox.y1))
        data_width    = data_coords_2[0] - data_coords_1[0]
        data_height   = data_coords_2[1] - data_coords_1[1]
        minmax.add(LTPoint(flag_x, flag_y) + LTPoint(data_width, data_height))

    MARGIN = 5
    ax.set_xlim(minmax.min.x - MARGIN, minmax.max.x + MARGIN)
    ax.set_ylim(minmax.min.y - MARGIN, minmax.max.y + MARGIN)    
    ax.invert_yaxis()

    return {
        'components'        : components,
        'wires'             : wires,
        'points_to_wires'   : points_to_wires,
        'points_to_pins'    : points_to_pins,
        'name_to_component' : name_to_component,
        'pins'              : pins
    }


if __name__ == "__main__":
    import sys

    test_file_names = [
        "/home/james/Draft4.asc",
        "../../src/images/jeh-tech/electronics_common_emitter_amplifier.asc",
        "/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ground_up.asc",
        "/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/inductors.asc",
        "/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/one_rotated_inductor.asc",
        "/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ne555s.asc",
        "../../src/images/jeh-tech/electronics_nmos_depletion.asc",
        "/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ground.asc",
        "/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/iopin.asc"]

    if len(sys.argv) > 1:
        test_file_names = [sys.argv[1]]

    
    #with pl.xkcd(randomness=0, scale=.1, length=100):
    for filename in test_file_names:
        pl.rcParams['font.size'] = 14
        fig, ax = pl.subplots()
        try:
            d = lt_plot_asc(fig, ax, filename)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
            


        except Exception as exc:
            print(f"FAILED TO DRAW {filename} because {exc}")
            raise
        except:
            print(f"FAILED TO DRAW {filename}")
            raise
        print(d['name_to_component'])
        
        fig.show()
        pl.show()
        pl.close(fig)