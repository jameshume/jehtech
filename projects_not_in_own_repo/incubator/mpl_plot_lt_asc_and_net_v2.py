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
import matplotlib as mpl
import matplotlib.pyplot as pl
import ltspice
from netlist              import parse_netlist, NetComponent, Net
from mpl_plot_lt_asc_file import lt_plot_asc
from lt_shapes            import LTPin, LTPoint, LTLine
from lt_component         import LTComponent

mpl.rcParams['lines.linewidth'] = 2


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


#
# A netlist in LTSpice terms (PCBExpress format netlist to be precise as supported by `parse_netlist()`)

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
#                [C1:pin -> W1:pin, W1:pin -> W2:pin]
#                 /\
#                /  `-----------------
#               /                     \ 
#             [W2:pin -> W3:pin]    [W2:pin -> W4:pin]
#              |                      |
#              [W3:pin -> C2:pin]   [W4:pin -> C3:pin]
#
#

from dataclasses import dataclass, field

@dataclass
class TreeNode:
    is_component : bool
    data : list=field(default_factory=list)
    kids : list=field(default_factory=list)

    


colours = ['r', 'g', 'b', 'c', 'm', 'y']
def next_colour(colour_idx):
    global colours
    next_idx = colour_idx + 1
    if next_idx >= len(colours):
        next_idx = 0
    return next_idx

def plot_get_lt_wires_connected_to_point(plot_info, point : LTPoint):
    points2wires : dict[LTPoint, list[LTLine]] = plot_info['points_to_wires']
    return points2wires[point]

def plot_get_lt_component_from_part_id(plot_info, part_id :str):
    return plot_info["name_to_component"][part_id]        

def net_component_pin_to_lt_component_pin(net_component_pin : int, lt_component : LTComponent) -> LTPin:
    return lt_component.get_pin_by_spice_order(net_component_pin)

def plot_get_lt_wire_point_at_point(wire : LTLine, point : LTPoint):
    """
    """
    if

def donet(plot_info, net : Net):
    # Traverse from the head to each other component. 
    
    nc : NetComponent = nets[net_name].head
    
    head = TreeNode(is_component=True)
    head.data = None
    
    # From the netlist-component, get the part ID, and use this to lookup the LTComponent in the plot that corresponds
    # to this netlist-component.
    lt_component     : LTComponent  = plot_get_lt_component_from_part_id(nc.part.part_id)

    # A specific pin of the netlist-component is being considered. Map this to the pin in the LTComponent.
    lt_compenent_pin : LTPin        = net_component_pin_to_lt_component_pin(nc.pin, lt_component)

    # Now get all the wires (LTLine's) that have a point that connects to the LTComponent pin in question
    wire_list        : list[LTLine] = plot_get_lt_wires_connected_to_point(plot_info, lt_compenent_pin.p)

    # Create a child node for each of these wires
    for wire in wire_list:
        child = TreeNode(is_component=False)
        wire_point = 1 # get_lt_wire_pin_at_point()
        child.data = [((lt_component, lt_compenent_pin), (wire, wire_point))]
        # Now add into child.data all wires that do not branch to > 1 wire.
        child.data.append(add_all_non_branching_wires(wire))

with pl.xkcd():
    fig, ax = pl.subplots()
    
    # Parse the .raw file
    l = ltspice.Ltspice(raw_filename) 
    l.parse() 


    # What I want is for the LTShape objects to be extended to have setColour, setBlahBlahBlah methods that
    # will allow the figure and axis artists to update their drawings.
    plot_info = lt_plot_asc(fig, ax, asc_filename)

    
    
    colour_idx = 0
    for net_name in nets:        
        donet(plot_info, nets[net_name])

        

       
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for spine in ax.spines:
        ax.spines[spine].set_visible(False)

    fig.show()
    pl.show()
    pl.close(fig)