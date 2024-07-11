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

## To install XKCD fonts on Linux use this:
##  $ mkdir -p ~/.local/share/fonts
##  $ curl -sL https://github.com/ipython/xkcd-font/raw/master/xkcd-script/font/xkcd-script.ttf -o ~/.local/share/fonts/xkcd-script.ttf
##  $ fc-cache -f -v
##  $ rm ~/.cache/matplotlib/*
#
# Also, dunno what the difference between xkcd-script and just xkcd is in terms of fonts but needed to cop xkcd-script as xkcd and
# update ~/.cache/matplotlib/fontlist-v330.json  so its was called just "xkcd" to get rid of sily font warnings.
##
##  $ apt install fonts-humor-sans
##  $ rm -r ~/.cache/matplotlib

import sys
import pprint
import matplotlib.pyplot as pl
import ltspice
import subprocess
from netlist              import parse_netlist, NetComponent
from mpl_plot_lt_asc_file import lt_plot_asc
from lt_shapes            import LTPin, LTPoint, LTLine

if len(sys.argv) == 1:
    net_filename = "simple_circult_netlist.net"
    asc_filename = "simple_circult_netlist.asc"
    raw_filename = "simple_circult_netlist.raw"
else:
    asc_filename = sys.argv[1]
    net_filename = sys.argv[1][:-3] + "net"
    raw_filename = sys.argv[1][:-3] + "raw"



nets = parse_netlist(net_filename)
pprint.pp(nets)



import enum
class dfs_result_t (enum.Enum):
    DFS_STOP_FOUND_EP     = enum.auto()
    DFS_STOP_NOT_FOUND_EP = enum.auto()

def depth_first_net_traverse(
        current_point : LTPin,
        end_point     : LTPin, 
        wire_list     : list[LTLine], 
        points2wires  : dict[LTPoint, list[LTLine]],
        depth         : int) -> dfs_result_t:

    print(f"{' ' * (depth * 4)}depth_first_net_traverse({current_point}, ..., {depth})")

    if current_point == end_point:
        return dfs_result_t.DFS_STOP_FOUND_EP

    # Get all the wires with one point joining the `current_point``
    wires : list(LTLine) = points2wires[current_point]

    # Search this list for a wire that has not been visited and leads to an end point
    next_point = None
    path_found = False
    for wire in wires:
        print(f"{' ' * (depth * 4 + 2)} Checking {wire}")
        if wire._visited is False:
            wire._visited = True
            if wire.p1 == current_point:
                next_point = wire.p2
            else:
                next_point = wire.p1
            
            result = depth_first_net_traverse(next_point, end_point, wire_list, points2wires, depth+1)
            if result == dfs_result_t.DFS_STOP_FOUND_EP:
                wire_list.insert(0, wire)
                path_found = True
                break

    return dfs_result_t.DFS_STOP_FOUND_EP if path_found else dfs_result_t.DFS_STOP_NOT_FOUND_EP



def build_net(c1 : NetComponent, c2 : NetComponent):
    # c1, c2 are the connected component's, and the associated pin, that are connected in the net.
    # Get the LTComponent objects that represent the net-list components c1 and c2.
    lt_component_1 : LTComponent = drawing["name_to_component"][c1.part.part_id]
    lt_component_2 : LTComponent = drawing["name_to_component"][c2.part.part_id]

    # lt_cx_pin are the LTPin objects associated with the component from the netlist, tying together
    # the netlist and the asc file
    lt_c1_pin : LTPin = lt_component_1.get_pin_by_spice_order(c1.pin)
    lt_c2_pin : LTPin = lt_component_2.get_pin_by_spice_order(c2.pin)

    # now find out the sequenc of wires that connect c1 to c2 by doing a depth first search of the
    # tree, which I'm assuming is acyclic at the moment.
    points2wires  : dict[LTPoint, list(LTLine)] = drawing['points_to_wires']

    for point in points2wires:
        for wire in points2wires[point]:
            wire._visited = False

    wire_list = []
    result = depth_first_net_traverse(current_point=lt_c1_pin.p, end_point=lt_c2_pin.p, wire_list=wire_list, points2wires=points2wires, depth=0)
    return result, wire_list


colours = ['r', 'g', 'b', 'c', 'm', 'y']
def next_colour(colour_idx):
    global colours
    next_idx = colour_idx + 1
    if next_idx >= len(colours):
        next_idx = 0
    return next_idx

with pl.xkcd():
    fig, ax = pl.subplots()
    
    # Parse the .raw file
    l = ltspice.Ltspice(raw_filename) 
    l.parse() 


    # What I want is for the LTShape objects to be extended to have setColour, setBlahBlahBlah methods that
    # will allow the figure and axis artists to update their drawings.
    drawing = lt_plot_asc(fig, ax, asc_filename)

    something = []
    colour_idx = 0
    for net_name in nets:
        colour_idx += 1
        # Want to build up a list of wires that join each component in the net
        print("-" * 40)
        print(f"{net_name}\n")

        # I want pairs (c1, c2), (c2, c3), ... 
        nc : NetComponent = nets[net_name].head
        pairs = []
        while nc is not None:
            pair = [None, None]
            while (nc is not None) and (pair[1] is None):
                if pair[0] is None:
                    pair[0] = nc
                    nc = nc.next
                else:
                    pair[1] = nc
                    pairs.append(pair)

        #
        # For each pair, find the wires that go between each pin
        # Example pair
        #    [
        #       NetComponent(part=Part(part_id='R1', part_name='R'),
        #                     pin=2,
        #                     next=...,
        #       NetComponent(part=Part(part_id='R2', part_name='R'), pin=2, next=None)
        #    ]
        #
        # Need to create a tree. The root is a component and so are all the leaves. Each tree node 
        # is a set of continuous wire segments that create one complete non-splitting path. Under
        # that node would be all the wires
        #
        #                    1      2      3
        # I.e. if we had C1------+------+------ C2
        #                               |  4
        #                               +------ C3
        # This will create the tree
        #                 C1
        #                 |
        #                [1,2]
        #                 /\
        #                /  \
        #               /    \
        #             [3]    [4]
        #              |      |
        #              C2     C3
        #
        # To show the currents, we then know the current propogates up from the leaves. At each node 
        # going upwards the current adds.
        #
        # Currently I get the one path. Need to merge them.
        #
        for c1, c2 in pairs:
            cap_time = l.get_time()
            cap_V_source = l.get_data(f'V({c1.part.part_id})')
            cap_I_source = l.get_data(f'I({c1.part.part_id})')
            cap_I_source2 = l.get_data(f'I({c2.part.part_id})')

            result, wires = build_net(c1, c2)
            something.append((c1, wires, c2))

            print(c1, c2)
            print(result)
            print(wires)
            for wire in wires:
                wire.set_colour(colours[colour_idx])
                colour_idx = next_colour(colour_idx)

    print("*"*100)
    pprint.pp(something)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)

    fig.show()
    pl.show()
    pl.close(fig)