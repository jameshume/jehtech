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
    nc : NetComponent = nets[net_name].head
    while nc is not None:
        print(drawing['name_to_component'][nc.part.part_id])
        nc = nc.next

#pprint.pp(drawing)
pl.close(fig)