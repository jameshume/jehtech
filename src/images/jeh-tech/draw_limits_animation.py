#
# Copyright (c) 2018 James Hume (www.jeh-tech.com). All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by James Hume (www.jeh-tech.com)
# 4. Neither the name "James Hume" or website "www.jeh-tech.com"
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.animation as animation

x = np.linspace(0,5,1000)
y = np.power(x,2)

fig, ax = pl.subplots()
line, = ax.plot(x,y)
ax.grid()
ax.axvline(x=3, linestyle=":")
ax.axhline(y=9, linestyle=":")
p1, = ax.plot(2.5, 2.5*2.5, marker="o")
txt1 = ax.text(2.5, 2.5*2.5, "{}".format(2.5*2.5), color=p1.get_color())
p2, = ax.plot(3.5, 3.5*3.5, marker="o")
txt2 = ax.text(3.5, 3.5*3.5, "{}".format(3.5*3.5), color=p2.get_color())

msg = ax.text(0,15,"We can approach x=3.0 from\nboth the left and the right", alpha=1.0, fontsize=20)

#framemsg = ax.text(3,0,"Start")

ax.set_title("Limits")

#pl.show()


xmin_orig, xmax_orig = ax.get_xlim()

# For long animations make sure you have matplot v2.2.1 or later
# https://github.com/matplotlib/matplotlib/issues/10729/
def animate(i):
    global ax, p1, txt1, p2, txt2, msg
    #global framemsg

    if i < 50:
        #framemsg.set_text("A{}".format(i))
        msg.set_alpha((i+1)/50)
    elif i < 100:
        #framemsg.set_text("B{}".format(i))
        i = i - 50
        x1 = 2.5 + i/100.0
        p1.set_xdata([x1])
        p1.set_ydata([x1 * x1])

        txt1.set_x(x1)
        txt1.set_y(x1 * x1)
        txt1.set_text("{:.4f}".format(x1 * x1))

        x2 = 3.5 - i/100.0
        p2.set_xdata([x2])
        p2.set_ydata([x2 * x2])

        txt2.set_x(x2)
        txt2.set_y(x2 * x2)
        txt2.set_text("{:.4f}".format(x2 * x2))
    elif i < 150:
        #framemsg.set_text("C{}".format(i))
        i = i - 100
        msg.set_alpha(1.0 - (i+1)/50)
    elif i < 200:
        #framemsg.set_text("D{}".format(i))
        i = i - 150
        msg.set_text("We get pretty close, and\nwe can ALWAYS zoom in...")
        msg.set_alpha(i/50)
    elif i < 250:
        #framemsg.set_text("E{}".format(i))
        pass
    elif i < 300:
        #framemsg.set_text("F{}".format(i))
        i = i - 250
        msg.set_alpha(1.0 - i/50)
    elif i < 350: 
        #framemsg.set_text("G{}".format(i))
        i = i - 300
        xmin_new = 2.989
        xmax_new = 3.011
        xmin_delta = (xmin_new - xmin_orig) / 49.0
        xmax_delta = (xmax_orig - xmax_new) / 49.0
        xmin, xmax = ax.get_xlim()
        ax.set_xlim([xmin_orig + i * xmin_delta, xmax_orig - i * xmax_delta])
    elif i < 375:
        #framemsg.set_text("H{}".format(i))
        pass
    elif i < 400:
        #framemsg.set_text("I{}".format(i))
        i = i - 375
        x1 = p1.get_xdata()[0] + 1/2700.0
        p1.set_xdata([x1])
        p1.set_ydata([x1 * x1])

        txt1.set_x(x1)
        txt1.set_y(x1 * x1)
        txt1.set_text("{:.4f}".format(x1 * x1))

        x2 = p2.get_xdata()[0] - 1/2700.0
        p2.set_xdata([x2])
        p2.set_ydata([x2 * x2])

        txt2.set_x(x2)
        txt2.set_y(x2 * x2)
        txt2.set_text("{:.4f}".format(x2 * x2))
    elif i < 450:
        #framemsg.set_text("J{}".format(i))
        i = i - 400
        msg.set_x(2.99)
        msg.set_text("We could zoom in even further.\nThe process never ends...\nwe can get as close as we like\nwithout ever reaching x=3!")
        msg.set_alpha((i+1)/50)
    elif i < 500:
        pass


Writer = animation.writers['ffmpeg']
writer = Writer(fps=25, metadata=dict(artist='James Hume @ www.jeh-tech.com'), bitrate=1800)
ani = animation.FuncAnimation(fig, animate, frames=550, blit=False, repeat=False)
ani.save('animation.mp4', writer=writer)
