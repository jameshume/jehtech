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

def draw_line_from_vector(v, ax, *args, **kwargs):
    bottom, top = ax.get_ylim()
    x_left, x_right = ax.get_xlim()

    # y = mx+c
    m = v[1]/v[0]
    c = v[1] - m * v[0]

    y_left  = m * x_left + c
    y_right = m * x_right + c

    ax.plot([x_left, x_right], [y_left, y_right], *args, **kwargs)

def draw_vec(v, ax, *args, **kwargs):
   ax.arrow(0, 0, v[0], v[1], length_includes_head=True, *args, **kwargs)


fig, ax = pl.subplots()
ax.set_xlim([-2,2])
ax.set_ylim([-2,2])
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.grid()
ax.set_title(r"Example 1: EigenSpaces for $\lambda = 5$ and $\lambda = -1$")
v1 = np.array([0.5, 1.0])
v2 = np.array([-1, 1])

draw_vec(v1, ax, lw=2, head_width=0.05, zorder=1, color='blue')
draw_vec(v2, ax, lw=2, head_width=0.05, zorder=1, color='red')

draw_line_from_vector(v1, ax, alpha=0.25, zorder=0, color='blue')
draw_line_from_vector(v2, ax, alpha=0.25, zorder=0, color='red')

fig.show()
pl.show()

