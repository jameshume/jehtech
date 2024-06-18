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
import pprint
import matplotlib.pyplot as pl
from netlist              import parse_netlist, NetComponent
from mpl_plot_lt_asc_file import lt_plot_asc

net_filename = "simple_circult_netlist.net"
asc_filename = "simple_circult_netlist.asc"

nets = parse_netlist(net_filename)
pprint.pp(nets)

fig, ax = pl.subplots()
drawing = lt_plot_asc(fig, ax, asc_filename)


for net_name in nets:
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

    # For each pair, find the wires that go between each pin
    # Example pair
    #    [
    #       NetComponent(part=Part(part_id='R1', part_name='R'),
    #                     pin=2,
    #                     next=...,
    #       NetComponent(part=Part(part_id='R2', part_name='R'), pin=2, next=None)
    #    ]
    for c1, c2 in pairs:
        # c1, c2 are the connected component's, and the associated pin, that are connected in the net.
        # Get the LTComponent objects that represent the net-list components c1 and c2.
        lt_component_1 = drawing["name_to_component"][c1.part.part_id]
        lt_component_2 = drawing["name_to_component"][c2.part.part_id]

        # lt_cx_pin are the LTPin objects associated with the component from the netlist, tying together
        # the netlist and the asc file
        lt_c1_pin = lt_component_1.get_pin_by_spice_order(c1.pin)
        lt_c2_pin = lt_component_2.get_pin_by_spice_order(c2.pin)

        # now find out the sequenc of wires that connect c1 to c2 by doing a depth first search of the
        # tree, which I'm assuming is acyclic at the moment.
        current_point = lt_c1_pin.p
        wire = drawing['points_to_wires'][current_point]
        while wire:
            print(current_point, wire)
            next_point = None
            if wire[0].p1 == current_point:
                next_point = wire[0].p2
            else:
                next_point = wire[0].p1
            wire = drawing['points_to_wires'][next_point] # This will contain the last wire, which we just visited and DONT want to do!
            current_point = next_point
            print(current_point, wire)

            break
        break

pl.close(fig)