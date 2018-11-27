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

x = np.linspace(-15,15,1000)
y = np.power(x,2)

def setup_axis(ax):
    ax.set_xlim([-15,15])
    ax.set_ylim([0,15])
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.grid()


fig, (ax, ax2, ax3) = pl.subplots(nrows = 3)
fig.set_size_inches(5, 10)



setup_axis(ax)
setup_axis(ax2)
setup_axis(ax3)
ax2.set_ylim([-15,15])

line, = ax.plot(x,y)
line2, = ax2.plot(x,y)
line3, = ax3.plot(x,y)
pl.subplots_adjust(wspace=15.)

def animate(i):
    global line, ax, line2, ax2, line3, ax3
    y = None
    y2 = None
    y3 = None
    if i < 10:
        ax.set_title('$y = (x + {})^2$'.format(i))
        y = np.power(x+i,2)

        ax2.set_title('$y = x^2 + {}$'.format(i))
        y2 = np.power(x,2) + i

        ax3.set_title('$y = ({}x)^2$'.format(i))
        y3 = np.power(i*x, 2)

    elif i < 20:
        ax.set_title('$y = (x + {})^2$'.format(20-i))
        y = np.power(x+(20-i),2)

        ax2.set_title('$y = x^2 + {}$'.format(20-i))
        y2 = np.power(x,2) + 20-i

        ax3.set_title('$y = ({}x)^2$'.format((20-i)))
        y3 = np.power((20-i)*x, 2)

    elif i < 30:
        ax.set_title('$y = (x - {})^2$'.format(i-20))
        y = np.power(x-(i-20),2)

        ax2.set_title('$y = x^2 - {}$'.format(i-20))
        y2 = np.power(x,2) - (i-20)

        ax3.set_title('$y = (x/{})^2$'.format(i-19))
        y3 = np.power((1./(i-19))*x, 2)

    else:
        ax.set_title('$y = (x - {})^2$'.format(40-i))
        y = np.power(x-(40-i),2)

        ax2.set_title('$y = x^2 - {}$'.format(40-i))
        y2 = np.power(x,2) - (40-i)

        ax3.set_title('$y = (x/{})^2$'.format(40-i))
        y3 = np.power((1./(40-i))*x, 2)

    line.set_ydata(y)
    line2.set_ydata(y2)
    line3.set_ydata(y3)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=2, metadata=dict(artist='James Hume @ www.jeh-tech.com'), bitrate=1800)
ani = animation.FuncAnimation(fig, animate, frames=40, interval=1, blit=False)
ani.save('animation.mp4', writer=writer)
