
#pip install ltspice spicelib
#conda install -c conda-forge ffmpeg
import ltspice
import numpy as np
import os
import sys  
import tempfile
import shutil
import subprocess
from spicelib import AscEditor 
import matplotlib.pyplot as pl
import matplotlib.animation as animation
import matplotlib.image as image
from matplotlib.gridspec import GridSpec

fig    = pl.figure(layout="constrained")
gs     = GridSpec(2, 2, figure=fig)
ax     = fig.add_subplot(gs[0, 0])
ax_i   = fig.add_subplot(gs[1, 0])
ax_pic = fig.add_subplot(gs[0:, 1])


line_V_source  = None
line_V_ind     = None
line_current   = None

ax.set_ylabel("Voltage (Volts)")
ax.grid()
ax.set_ylim(-5.5, 5.5)

ax_i.set_xlabel("Time (Seconds)")
ax_i.set_ylabel("Current (Amps)")
ax_i.grid()

im = image.imread("../electronics_pulse_into_indictor.png")
ax_pic.imshow(im)
ax_pic.set_axis_off()

NUM_FRAMES=10

with tempfile.TemporaryDirectory() as tmpdirname:
    shutil.copy("../electronics_pulse_into_indictor.asc", tmpdirname)
    print(os.listdir(tmpdirname))


    asc = AscEditor(f"{tmpdirname}/electronics_pulse_into_indictor.asc") 

    def animate(i):
        global line_V_source
        global line_V_ind
        global line_current
        global fig
        global ax
        global ax_i

        print(i)
        if i < NUM_FRAMES / 2:
            i = i
        else:
            i = (NUM_FRAMES - i)
      
        ax.set_title(f"L1 = {i}mH")
        asc.set_component_value("L1", f"{i}mL")
        asc.save_netlist(f"{tmpdirname}/electronics_pulse_into_indictor_mod.asc")

        x = subprocess.run(
            ["C:\\Users\\JamesHume\\AppData\\Local\\Programs\\ADI\\LTspice\\ltspice.exe", 
                "-Run", 
                "-b", 
                f"{tmpdirname}\\electronics_pulse_into_indictor_mod.asc"
            ], shell=True)

        l = ltspice.Ltspice(f"{tmpdirname}/electronics_pulse_into_indictor_mod.raw") 
        l.parse() 

        time = l.get_time()
        V_source = l.get_data('V(source)')
        I_source = l.get_data('I(R1)')
        V_ind = l.get_data('V(ind)')

        if line_V_source is None:
            line_V_source, = ax.plot(time, V_source)
            line_V_ind, = ax.plot(time, V_ind)
            line_current, = ax_i.plot(time, I_source)
        else:
            line_V_source.set_xdata([time])
            line_V_source.set_ydata([V_source])
            line_V_ind.set_xdata([time])
            line_V_ind.set_ydata([V_ind])
            line_current.set_xdata([time])
            line_current.set_ydata([I_source])

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='James Hume @ www.jehtech.com'), bitrate=1800)
    ani = animation.FuncAnimation(fig, animate, frames=NUM_FRAMES, blit=False, repeat=False)
    ani.save('electronics_pulse_into_ind_vary_inductance.mp4', writer=writer)        
