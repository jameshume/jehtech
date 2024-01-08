
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


fig, ((ax_cap_v, ax_ind_v), (ax_cap_i, ax_ind_i)) = pl.subplots(nrows=2, ncols=2)
line_cap_V_source  = None
line_cap_V_cap     = None
line_cap_I         = None
line_ind_V_source  = None
line_ind_V_ind     = None
line_ind_I         = None

ax_cap_v.set_ylabel("Voltage (Volts)")
ax_cap_v.grid()

ax_cap_i.set_xlabel("Time (Seconds)")
ax_cap_i.set_ylabel("Current (Amps)")
ax_cap_i.grid()

ax_ind_v.set_ylabel("Voltage (Volts)")
ax_ind_v.grid()

ax_cap_i.set_xlabel("Time (Seconds)")
ax_cap_i.set_ylabel("Current (Amps)")
ax_ind_i.grid()

NUM_FRAMES=200

with tempfile.TemporaryDirectory() as tmpdirname:
    shutil.copy("../electronics_pulse_into_cap.asc", tmpdirname)
    shutil.copy("../electronics_pulse_into_indictor.asc", tmpdirname)
    print(os.listdir(tmpdirname))

    asc_cap = AscEditor(f"{tmpdirname}/electronics_pulse_into_cap.asc") 
    asc_ind = AscEditor(f"{tmpdirname}/electronics_pulse_into_indictor.asc") 

    def animate(i):
        global line_cap_V_source
        global line_cap_V_cap
        global line_cap_I
        global line_ind_V_source
        global line_ind_V_ind
        global line_ind_I
  
        global fig
        global ax_cap_v
        global ax_cap_i
        global ax_ind_v
        global ax_ind_i

        i = i + 1

        print(i)
        if i < NUM_FRAMES/2:
            i_cap = i *  50
            i_ind = i
        else:
            i_cap = (NUM_FRAMES - i) * 50
            i_ind = (NUM_FRAMES - i)

        ax_cap_v.set_title(f"C1 = {i_cap}uF")
        ax_ind_v.set_title(f"L1 = {i_ind}mL")

        asc_cap.set_component_value("C1", f"{i_cap}uF")
        asc_cap.save_netlist(f"{tmpdirname}/electronics_pulse_into_cap_mod.asc")
        asc_ind.set_component_value("L1", f"{i_ind}mL")
        asc_ind.save_netlist(f"{tmpdirname}/electronics_pulse_into_indictor_mod.asc")

        x = subprocess.run(
            ["C:\\Users\\JamesHume\\AppData\\Local\\Programs\\ADI\\LTspice\\ltspice.exe", 
                "-Run", 
                "-b", 
                f"{tmpdirname}\\electronics_pulse_into_cap_mod.asc"
            ], shell=True)
        l = ltspice.Ltspice(f"{tmpdirname}/electronics_pulse_into_cap_mod.raw") 
        l.parse() 

        cap_time = l.get_time()
        cap_V_source = l.get_data('V(source)')
        cap_I_source = l.get_data('I(R1)')
        cap_V_cap = l.get_data('V(cap)')

        x = subprocess.run(
            ["C:\\Users\\JamesHume\\AppData\\Local\\Programs\\ADI\\LTspice\\ltspice.exe", 
                "-Run", 
                "-b", 
                f"{tmpdirname}\\electronics_pulse_into_indictor_mod.asc"
            ], shell=True)
        l = ltspice.Ltspice(f"{tmpdirname}/electronics_pulse_into_indictor_mod.raw") 
        l.parse()

        ind_time = l.get_time()
        ind_V_source = l.get_data('V(source)')
        ind_I_source = l.get_data('I(R1)')
        ind_V_ind = l.get_data('V(ind)')

        if line_cap_V_source is None:
            line_cap_V_source, = ax_cap_v.plot(cap_time, cap_V_source)
            line_cap_V_cap,    = ax_cap_v.plot(cap_time, cap_V_cap)
            line_cap_I,        = ax_cap_i.plot(cap_time, cap_I_source)
        else:
            line_cap_V_source.set_xdata([cap_time])
            line_cap_V_source.set_ydata([cap_V_source])
            line_cap_V_cap.set_xdata([cap_time])
            line_cap_V_cap.set_ydata([cap_V_cap])
            line_cap_I.set_xdata([cap_time])
            line_cap_I.set_ydata([cap_I_source])

        if line_ind_V_source is None:
            line_ind_V_source, = ax_ind_v.plot(ind_time, ind_V_source)
            line_ind_V_ind,    = ax_ind_v.plot(ind_time, ind_V_ind)
            line_ind_I,        = ax_ind_i.plot(ind_time, ind_I_source)
        else:
            line_ind_V_source.set_xdata([ind_time])
            line_ind_V_source.set_ydata([ind_V_source])
            line_ind_V_ind.set_xdata([ind_time])
            line_ind_V_ind.set_ydata([ind_V_ind])
            line_ind_I.set_xdata([ind_time])
            line_ind_I.set_ydata([ind_I_source])

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='James Hume @ www.jehtech.com'), bitrate=1800)
    ani = animation.FuncAnimation(fig, animate, frames=NUM_FRAMES, blit=False, repeat=False)
    ani.save('electronics_pulse_into_cap_vs_ind.mp4', writer=writer)        
