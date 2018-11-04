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

v2              = np.array([ 2, 4 ])
v1              = np.array([ 4, 2 ])
v2_onto_v1      = (np.dot(v2, v1) / np.linalg.norm(v1) ** 2) * v1;
v2_onto_v1_perp = v2 - v2_onto_v1


pl.quiver(0, 0, v2[0], v2[1], color='r', angles='xy', scale_units='xy', scale=1)
pl.quiver(0, 0, v1[0], v1[1], color='b', angles='xy', scale_units='xy', scale=1)
pl.quiver(4, 2, v2[0], v2[1], angles='xy', color='r', scale_units='xy', scale=1, alpha=0.5)

pl.quiver(2, 4, v1[0], v1[1], angles='xy', color='b', scale_units='xy', scale=1, alpha=0.5)
pl.quiver(0, 0, v2_onto_v1[0], v2_onto_v1[1], angles='xy', color='c', scale_units='xy', scale=1)
pl.quiver(v2_onto_v1[0], v2_onto_v1[1], v2_onto_v1_perp[0], v2_onto_v1_perp[1], angles='xy', color='purple', scale_units='xy', scale=1)
pl.fill([0, 2, 6, 4], [0, 4, 6, 2], color="yellow", alpha=0.3)

pl.text(5, 6.5, "The area of the parallelogram is\nthe determinant of the matrix\nformed by the column vectors\nv2 and v1", ha="left", fontsize='medium')
pl.annotate( r""
           , xy=(5,5)
           , xytext=(30, 35)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='black', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="w")
)

pl.annotate( r"$\mathrm{proj}_{\vec{v1}}(\vec{v2})$"
           , xy=(2,1)
           , xytext=(30, -20)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='black', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="w"))

pl.annotate( r"$\vec{v2} - \mathrm{proj}_{\vec{v1}}(\vec{v2})$"
           , xy=(2.5,3)
           , xytext=(30, 20)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='black', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="w"))

pl.annotate( r"$\vec{v1}$"
           , xy=(3.6,1.8)
           , xytext=(60, -5)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='black', shrink=0.05, connectionstyle="arc3,rad=-0.3", fc="w"))

pl.annotate( r"$\vec{v2}$"
           , xy=(1.2,2.3)
           , xytext=(-30, 30)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='black', shrink=0.05, connectionstyle="arc3,rad=0.2", fc="w"))
  
pl.xlim(0, 10)
pl.ylim(0, 9)

pl.show()

