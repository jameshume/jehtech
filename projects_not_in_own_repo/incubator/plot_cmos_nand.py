import matplotlib.pyplot as pl
from mpl_plot_lt_asc_file import lt_plot_asc

#with pl.xkcd(randomness=0, scale=.1, length=100):

filename = "../../src/images/jeh-tech/electronics_cmos_nand.asc"

fig, ax = pl.subplots()
try:
    d = lt_plot_asc(fig, ax, filename)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    
    top_net_from_vcc = d['wires'][0:5]
    for wire in top_net_from_vcc: wire.set_colour('red')
    top_net_from_vcc[3].set_colour('blue')

    a_input_net = d['wires'][5:7] + d['wires'][17:19]
    for wire in a_input_net: wire.set_colour('red')
    d['pins']['A'].set_colour('red')
    
    b_input_net = d['wires'][7:11] + d['wires'][20:22]
    for wire in b_input_net: wire.set_colour('blue')
    d['pins']['B'].set_colour('blue')
                
    m1_m2_to_m3_and_out_net = d['wires'][11:17]
    for wire in m1_m2_to_m3_and_out_net: wire.set_colour('blue')
    d['pins']['Out'].set_colour('blue')

    m3_to_m4_net = d['wires'][19:20]
    for wire in m3_to_m4_net: wire.set_colour('blue')

    m4_to_groupd_net = d['wires'][22:23]
    for wire in m4_to_groupd_net: wire.set_colour('blue')


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