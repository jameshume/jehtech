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
import matplotlib.pyplot as pl
import numpy as np
import matplotlib.animation as animation
import math
import sys

fig, ax = pl.subplots()
ns_quiv = None
psol_quiv = None
ns_txt = None
psol_txt = None
ns_vec_scalar = 0
state = "up"

def draw_quiv(o, v, c, z):
	return ax.plot([o[0], o[0] + v[0]], [o[1], o[1] + v[1]], color=c, zorder=z, lw=3)[0]
	#return ax.quiver(o[0], o[1], v[0], v[1], color=c, angles='xy', scale_units='xy', scale=1, zorder=z)


def init():
    global ns_quiv
    global ns_vec
    global psol_quiv
    global psol_vec
    global ns_txt
    global psol_txt
    global ns_vec_scalar

    z_vec         = np.array([0., 0.])
    ns_vec        = np.array([2./3., 1.])
    psol_vec      = np.array([3., 0.])

    # Quivers to draw the null space vector and the particular solution that we will
    # animate.
    ns_quiv   = draw_quiv(z_vec, ns_vec, 'r', 2)
    psol_quiv = draw_quiv(ns_vec, psol_vec, 'cyan', 2)
    
    # Plot lines representing the null space, row space and solution set.
    # They go "off" the x/y axis limits to make them look infinite.
    ax.plot([-10, 10], [-15, 15], color='r', zorder=0, alpha=0.5)
    ax.plot([-10, 10], [20.0/3.0, -20.0/3.0], color='b', zorder=0, alpha=0.5)
    ax.plot([-7, 13], [-15, 15], color='g', zorder=0, alpha=0.5)

    # Draw grid and set limits so that the space lines look infinite
    ax.grid();
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    ns_txt   = ax.text((ns_vec / 2.)[0], (ns_vec / 2.)[1], r'$\alpha \vec{n_o}\in \mathrm{N}(A)$')
    psol_txt = ax.text((psol_vec / 2 + ns_vec)[0], (psol_vec / 2 + ns_vec)[1], r'$[3, 0]$')

    ax.annotate( r'Solution set'
               , xy=(.75, -3.4)
               , xytext=(10, -40)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='green', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="g", alpha=0.5)
    )

    ax.annotate( r'$\mathrm{N}(A)$'
               , xy=(-2, -3)
               , xytext=(-10, 35)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='red', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="r", alpha=0.5)
    )

    ax.annotate( r'$\mathrm{C}(A^T)$'
               , xy=(-3, 2)
               , xytext=(-30, -40)
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(facecolor='blue', shrink=0.05, connectionstyle="arc3,rad=-0.1", fc="b", alpha=0.5)
    )

def animate(i):
    global ns_quiv
    global ns_vec
    global psol_quiv
    global psol_vec
    global ns_txt
    global psol_txt
    global ns_vec_scalar
    global state

    if state == "up":
      ns_vec_scalar += .1
      if ns_vec_scalar > 3.:
        state = "down"
    else:
      ns_vec_scalar -= .1
      if ns_vec_scalar < -4.9:
        state = "up"

    ns_scaled_vec = ns_vec * ns_vec_scalar
    ns_quiv.set_xdata([0, ns_scaled_vec[0]])
    ns_quiv.set_ydata([0, ns_scaled_vec[1]])

    psol_quiv.set_xdata([ns_scaled_vec[0], ns_scaled_vec[0] + psol_vec[0]])
    psol_quiv.set_ydata([ns_scaled_vec[1], ns_scaled_vec[1] + psol_vec[1]])

    ns_txt.set_x((ns_scaled_vec / 2.)[0])
    ns_txt.set_y((ns_scaled_vec / 2.)[1])
    psol_txt.set_x((psol_vec / 2 + ns_scaled_vec)[0])
    psol_txt.set_y((psol_vec / 2 + ns_scaled_vec)[1])

    return psol_quiv

# init()
# pl.show()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='James Hume @ www.jeh-tech.com'), bitrate=1800)
ani = animation.FuncAnimation(fig, animate, frames= 30*2 + 49*2+2, init_func=init, interval=100, blit=False)
ani.save('animation.mp4', writer=writer)

