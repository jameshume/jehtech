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
import numpy as np

##
## Project a vector onto the line defined by the vector v
## x - vector (numpy array) to be projected onto the line L
## v - vector (numpy array) defining the line L: L = {a * v}
def proj_x_onto_L(x, v):
    return (x.dot(v) / np.power(np.linalg.norm(v), 2)) * v

##
## Plot a 2D vector starting at an origin
## vec - vector (array or list) to plot, starting at origin
## origin - origin point of vector
def plot_vec(vec, origin, *args, **kwargs):
    if origin is not None:
        return ax.plot([origin[0], origin[0] + vec[0]], [origin[1], origin[1] + vec[1]], *args, **kwargs)[0]
    else:
        return ax.plot([0, vec[0]], [0, vec[1]], *args, **kwargs)[0]

##
## Plot 2D line plane
##
## Get the limits of the x-axis and plot a line that spans the entire x-axis to make
## the line look "infinite"
##
## vec - Vector (array or list) defining the line vector m if L = {a * m + b}
## yintercept - This is b if L = {a * m + b}
def plot_line_plane(vec, yintercept, *args, **kwargs):
    xmin, xmax = ax.get_xlim()
    m = vec[1]/vec[0]
    ymin = xmin * m + yintercept
    ymax = xmax * m + yintercept

    return ax.plot([xmin, xmax], [ymin, ymax], *args, **kwargs)[0]

def annotate_line(line, annotate_at_x, annotate_txt, xytext):
    x1, x2 = line.get_xdata()
    y1, y2 = line.get_ydata()
    
    m = (y2 - y1) / (x2 - x1)
    yintercept = y1 - m*x1

    pl.annotate( annotate_txt
               , xy=(annotate_at_x, annotate_at_x * m + yintercept)
               , xytext=xytext
               , textcoords='offset points'
               , fontsize='medium'
               , arrowprops=dict(shrink=0.05, connectionstyle="arc3,rad=0.1", fc=line.get_color())
    )

##
## Setup figure and axis so that graph axis at (0,0) and so that x/y limits 
## leave enough room to make figure look "good"
fig, ax = pl.subplots()
ax.set_xlim([-1.5, 2.5])
ax.set_ylim([-0.5, 2.5])
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.set_title('Projections calculated using data transformations to make LSS pass\nthrough origin. After projection onto LSS through origin everything\ntranslated back')

##
## Define noisy data points
data_points = [
    np.array([-1, 0]),
    np.array([0, 1]),
    np.array([1, 2]),
    np.array([2, 1])
]

##
## A color for each noisey data point
colours = ['red', 'green', 'blue', 'purple']

##
## Define the least squares solution
lss_vec = np.array([1., 2./5.])
lss_yintercept = np.array([0, 4./5.])

##
## Apply the translation that would bring the LSS line to the origin to all the data points
for i in range(len(data_points)):
    data_points[i] = data_points[i] - lss_yintercept

##
## Build projection of each data point vector onto LSS
projections = []
for dp in data_points:
    projections.append(proj_x_onto_L(dp, lss_vec))    

##
## Build the orthogonal line from each point to its projection on the LSS line
orthogs = []
for dp, p in zip(data_points, projections):
    orthogs.append(p - dp)

##
## Apply the inverse of the translation that would bring the LSS line to the origin to 
## all the data points, to put them back where they should be
for i in range(len(data_points)):    
    data_points[i] = data_points[i] + lss_yintercept

##
## Plot the data points
for i, (dp, c) in enumerate(zip(data_points, colours)):
    ax.plot(dp[0], dp[1], 'x', color=c)
    ax.text(dp[0], dp[1] + 0.03, '$\\vec{{d_{}}}$'.format(i), color=c)

##
## Plot the least squares solution line
lss_line = plot_line_plane(lss_vec, lss_yintercept[1], color='grey')

##
## Plot the projections - and here we see that the projections are onto the line
## passing through the origin, because to project onto a vector, it must pass through
## the origin because if L = c \vec{v}, for all real c's, when c is zero, it passes
## through origin.
for dp, p, orth, c in zip(data_points, projections, orthogs, colours):
    print(orth)
    plot_vec(orth, dp, color=c, alpha=0.5)

annotate_line(lss_line, -1.25, r'Least squares solution', (-40, 35))

fig.show()
pl.show()
