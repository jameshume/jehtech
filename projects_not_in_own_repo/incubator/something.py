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
        # c1, c2 are the connected component's, and the associated pin, that are connected in the net
        lt_component = drawing["name_to_component"][c1.part.part_id]

        # lt_cx_pin are the LTPin objects associated with the component from the netlist, tying together
        # the netlist and the asc file
        lt_c1_pin = lt_component.get_pin_by_spice_order(c1.pin)
        lt_c2_pin = lt_component.get_pin_by_spice_order(c2.pin)

        # now find out the sequenc of wires that connect c1 to c2 by doing a depth first search of the
        # tree, which I'm assuming is acyclic at the moment.
        print(drawing['points_to_wires'])
        print([lt_c1_pin.p])
        break

pl.close(fig)