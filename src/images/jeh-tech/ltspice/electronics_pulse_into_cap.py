
#pip install ltspice spicelib
import ltspice
import matplotlib.pyplot as plt
import numpy as np
import os
import sys  
import tempfile
import shutil
import subprocess
from spicelib import AscEditor 

with tempfile.TemporaryDirectory() as tmpdirname:
    shutil.copy("../electronics_pulse_into_cap.asc", tmpdirname)
    print(os.listdir(tmpdirname))

    asc = AscEditor(f"{tmpdirname}/electronics_pulse_into_cap.asc") 
    print(asc.get_component_info("C1"))
    asc.set_component_value("C1", "0.5mF")
    asc.save_netlist(f"{tmpdirname}/electronics_pulse_into_cap_mod.asc")

    x = subprocess.run(
        ["C:\\Users\\JamesHume\\AppData\\Local\\Programs\\ADI\\LTspice\\ltspice.exe", 
        "-Run", 
        "-b", 
        f"{tmpdirname}\\electronics_pulse_into_cap_mod.asc"], shell=True)
    print(x)
    print(os.listdir(tmpdirname))

    l = ltspice.Ltspice(f"{tmpdirname}/electronics_pulse_into_cap_mod.raw") 
    # Make sure that the .raw file is located in the correct path
    l.parse() 

    time = l.get_time()
    V_source = l.get_data('V(source)')
    V_cap = l.get_data('V(cap)')

    plt.plot(time, V_source)
    plt.plot(time, V_cap)
    plt.show()



