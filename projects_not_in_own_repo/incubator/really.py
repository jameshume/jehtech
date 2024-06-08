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

from plotasc import matplotlib_plot_component
from lt_shapes import LTPoint, LTLine
from lt_component import LTComponent

fig, ax = pl.subplots()
ax.invert_yaxis()

state = "normal"

flag_x, flag_y, flag_type = None, None, None

prev_line_cache = None

def parse_flag_line(line, draw=True):
    flag_x, flag_y, flag_type = line.strip().split(" ")[1:]
    flag_x, flag_y = (float(flag_x), float(flag_y))
    
    if flag_type == "0":
        if draw:
            circle1 = mpatches.Circle((flag_x, flag_y), 1, color='r')
            ax.add_patch(circle1)
            hw = 20
            h = 20
            ax.plot([flag_x - hw, flag_x + hw], [flag_y, flag_y], c='b')
            ax.plot([flag_x - hw, flag_x], [flag_y, flag_y + h], c='b')
            ax.plot([flag_x, flag_x + hw], [flag_y + h, flag_y], c='b')
    else:
        print(f"##### Flag type {flag_type} not supported")

    return flag_x, flag_y, flag_type

first_line = True

wires = []

#for line in open("/home/james/Draft4.asc"): #../../src/images/jeh-tech/electronics_lc_tank.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/inductors.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/one_rotated_inductor.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ne555s.asc"):
for line in open("../../src/images/jeh-tech/electronics_nmos_depletion.asc"):
#for line in open("../../src/images/jeh-tech/electronics_common_emitter_amplifier.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/ground.asc"):
#for line in open("/home/james/Repos/jehtech/projects_not_in_own_repo/incubator/iopin.asc"):
#for line in open("../../src/images/jeh-tech/wires.asc"):
    if (prev_line_cache is not None):
        if line.startswith("IOPIN "):
            x, y, inout = line.strip().split(" ")[1:]
            x, y = float(x), float(y)
            h = 20
            warrow = 20
            wbody = 20
            if inout == "Out":
                ax.plot([x, x - warrow], [y, y - h], c='b')
                ax.plot([x, x - warrow], [y, y + h], c='b')
            elif inout == "In":
                ax.plot([x, x + warrow], [y, y - h], c='b')
                ax.plot([x, x + warrow], [y, y + h], c='b')
            else:
                print(f"##### IO pin type {inout} not supported")

            flag_x, flag_y, flag_text = parse_flag_line(prev_line_cache, draw=False)
            ax.annotate(flag_text, xy=(x,y))
        else:
            parse_flag_line(prev_line_cache)
        
        prev_line_cache = None

    first_line = False

    
    if line.startswith("WIRE "):
        x1, y1, x2, y2 = [float(x) for x in line.strip().split(" ")[1:]]
        wires.append(LTLine(LTPoint(x1, y1), LTPoint(x2, y2)))
        ax.plot([x1, x2], [y1, y2], color='blue')


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
        name = tokens[0]
        x = float(tokens[1])
        y = float(tokens[2])
        rotation = float(tokens[3][1:])
        name = name.replace("\\", "/")
        totalname = f"/home/james/.wine/drive_c/Program Files/LTC/LTspiceXVII/lib/sym/{name}.asy"
        matplotlib_plot_component(LTComponent(totalname), ax, x, y, rotation)

if prev_line_cache is not None:
    prev_line_cache = None
    parse_flag_line(line)

# When a line has a connection to it, if the connection is in the middle of the line,
# it is broken into two. This means that lines that intersect do so at the start
# or finish of the line, never in the "middle" of a line. Thus, connections
# occur when a line starts/ends where another line starts/ends
#
# A really simple approach, if inefficient, is to say, for each line, find all lines
# that start/finish at either the start or finish of this line. If that line exists
# puts a "join" blob.
wire_nets = []
points_to_nets = {}
points = []
for i, wirei in enumerate(wires):
    for j, wirej in enumerate(wires):
        if i == j:
            continue

        if wirei.p1 == wirej.p1 and wirei.p1 not in points_to_nets:
            ax.add_patch(mpatches.Circle(wirei.p1.as_tuple(), 3, color='darkblue'))
            # Add this join p1 --- p1. Want to store the join point.
            # ((wirei, wirej), (p1, p1))
            # ((wirei, wirej), (p1, p2))
            # ((wirei, wirej), (p2, p1))
            # ((wirei, wirej), (p2, p2))
            #
            # We'd have to search for p1 in the sets of all other joins. If found add it there.
            # So, dictionary of points to nets? Then lookup and add to net.
            # 
            # But we would need to check to see if this wire is any other joins....
            # If it is we have to add it there 
            if wirei.p1 in points_to_nets:
                p2n = ((wirei, wirej), (p1, p1))
                points.append(p2n)
                points_to_nets[wirei.p1].append(p2n)
            else:
                p2n = ((wirei, wirej), (p1, p1))
                points.append(p2n)
                points_to_nets[wirei.p1] = [p2n]
            

        if wirei.p1 == wirej.p2 and wirei.p1 not in points_to_nets:
            ax.add_patch(mpatches.Circle(wirei.p1.as_tuple(), 3, color='darkblue'))
            if wirei.p1 in points_to_nets:
                points_to_nets[wirei.p1].append(((wirei, wirej), (p1, p2)))
                points_to_nets[wirei.p2].append(((wirei, wirej), (p1, p2)))
            else:
                points_to_nets[wirei.p1] = [((wirei, wirej), (p1, p2))]
                points_to_nets[wirei.p2] = [((wirei, wirej), (p1, p2))]

        if wirei.p2 == wirej.p1 and wirei.p2 not in points_to_nets:
            ax.add_patch(mpatches.Circle(wirei.p2.as_tuple(), 3, color='darkblue'))

        if wirei.p2 == wirej.p2 and wirei.p2 not in points_to_nets:
            ax.add_patch(mpatches.Circle(wirei.p2.as_tuple(), 3, color='darkblue'))
        


ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
ax.spines[['left', 'bottom', 'right', 'top']].set_visible(False)
ax.set_xticks([]) 
ax.set_yticks([]) 
ax.invert_yaxis()
fig.show()
pl.show()