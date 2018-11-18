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
import matplotlib.animation as animation
import itertools
import matplotlib.ticker as plticker

fig, ax = pl.subplots()

ax.set_xlim([-1,3])
ax.set_ylim([-1,3])
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')


grid2_colour='darkgray'
grid2_alpha=0.0
grid2 = []
for y1, y2 in zip(range(-8, 3), range(-2, 9)):
	l, = ax.plot([-3,3], [y1,y2], linewidth=1.0, color=grid2_colour, alpha=grid2_alpha)
	grid2.append(l)
for y1 in range(-2, 3):
	l, = ax.plot([-3,3], [y1,y1], linewidth=1.0, color=grid2_colour, alpha=grid2_alpha)
	grid2.append(l)


ax.plot([0, 2], [0, 2], color='r', alpha=0.75, zorder=2, lw=3)
loc = plticker.MultipleLocator(base=1.0)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)
ax.grid(False)

v1, = ax.plot([2, 2], [0, 1], color='lawngreen', zorder=2, lw=3, alpha=0.0, linestyle="--")
v2, = ax.plot([2, 2], [1, 2], color='lawngreen', zorder=2, lw=3, alpha=0.0, linestyle="--")

v3, = ax.plot([0, 1], [0, 0], color='lawngreen', zorder=2, lw=3, alpha=0.0, linestyle="--")
v4, = ax.plot([1, 2], [0, 0], color='lawngreen', zorder=2, lw=3, alpha=0.0, linestyle="--")

v5, = ax.plot([0, 1], [0, 1], color='lawngreen', zorder=2, lw=3, alpha=0.0, linestyle="--")
v6, = ax.plot([1, 2], [1, 2], color='lawngreen', zorder=2, lw=3, alpha=0.0, linestyle="--")

t1 = ax.text(2.1,2.1, r'$2\hat i + 2\hat j \rightarrow (2, 2)$', alpha=1.0, fontsize="13")
t2 = ax.text(2.1,2.1, r'$2\hat{v_1} + 0\hat{v_2}\rightarrow (2, 0)_B$', alpha=0.0, fontsize="13")

FRAME = 0
FPS=15
FADE_IN_TIME = FPS * 2 #2 seconds

def fade_in(step, total_steps, item):
	item.set_alpha(float(step)/float(total_steps))

def show(step, total_steps, item):
	item.set_alpha(1.0)

def hide(step, total_steps, item_array):
	for item in item_array:
		item.set_alpha(float(total_steps-step)/float(total_steps))

def grid1_on(step, total_steps, item_array):
	ax.grid(True, alpha=float(step)/float(total_steps))

def grid1_off(step, total_steps, item_array):
	ax.grid(False, alpha=float(total_steps-step)/float(total_steps))

def grid2_on(step, total_steps, item_array):
	for l in grid2:
		l.set_alpha(float(step)/float(total_steps))

def grid2_off(step, total_steps, item_array):
	for l in grid2:
		l.set_alpha(float(total_steps-step)/float(total_steps))

# Timeline - list of object - start time, end time
TIMELINE = [
	{'start' : 0 * FPS, 'end' : 1 * FPS -1, 'item' : v3, 'func' : grid1_on},
	{'start' : 0 * FPS, 'end' : 1 * FPS -1, 'item' : v3, 'func' : grid2_off},
	{'start' : 1 * FPS, 'end' : 2 * FPS -1, 'item' : v3, 'func' : fade_in},
	{'start' : 2 * FPS, 'end' : 3 * FPS -1, 'item' : v4, 'func' : fade_in},
	{'start' : 3 * FPS, 'end' : 4 * FPS -1, 'item' : v1, 'func' : fade_in},
	{'start' : 4 * FPS, 'end' : 5 * FPS -1, 'item' : v2, 'func' : fade_in},
	{'start' : 5 * FPS, 'end' : 6 * FPS -1, 'item' : [v1,v2,v3,v4,t1], 'func' : hide},
	{'start' : 6 * FPS, 'end' : 7 * FPS -1, 'item' : ax, 'func' : grid1_off},
	{'start' : 6 * FPS, 'end' : 7 * FPS -1, 'item' : ax, 'func' : grid2_on},
	{'start' : 6 * FPS, 'end' : 7 * FPS   , 'item' : t2, 'func' : show},
	{'start' : 7 * FPS, 'end' : 8 * FPS -1, 'item' : v5, 'func' : fade_in},
	{'start' : 8 * FPS, 'end' : 9 * FPS -1, 'item' : v6, 'func' : fade_in},
	{'start' : 10 * FPS, 'end' : 11 * FPS -1, 'item' : [v5,v6,t2], 'func' : hide},
]

ACTIVE = []

def animate(i):
	global FRAME, TIMELINE, ACTIVE

	for item in TIMELINE:
		if item['start'] == FRAME:
			ACTIVE.append(item)
	TIMELINE[:] = [item for item in TIMELINE if item['start'] > FRAME]

	ACTIVE[:] = [item for item in ACTIVE if FRAME <= item['end']]
	for item in ACTIVE:
		item['func'](
			FRAME - item['start'],
			item['end'] - item['start'],
			item['item'])
	
	FRAME += 1

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='James Hume @ www.jeh-tech.com'), bitrate=1800)
ani = animation.FuncAnimation(fig, animate, frames = FPS * 11,  interval=100, blit=False)
ani.save('animation.mp4', writer=writer)
