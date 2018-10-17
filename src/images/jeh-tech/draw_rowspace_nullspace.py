import matplotlib.pyplot as pl
import numpy as np

v2              = np.array([ 2, 4 ])
v1              = np.array([ 4, 2 ])
v2_onto_v1      = (np.dot(v2, v1) / np.linalg.norm(v1) ** 2) * v1;
v2_onto_v1_perp = v2 - v2_onto_v1




pl.quiver(0, 0, 2./3., 1, color='r', angles='xy', scale_units='xy', scale=1)
pl.quiver(3, 0, 2./3., 1, color='g', angles='xy', scale_units='xy', scale=1)
pl.quiver(0, 0, 1, -2./3., color='b', angles='xy', scale_units='xy', scale=1)
pl.quiver(0, 0, 3, 0, color='cyan', angles='xy', scale_units='xy', scale=1)

pl.quiver(0, 0, -18./5., -2./3. * -18./5., color='black', angles='xy', scale_units='xy', scale=1)

pl.plot([-10, 10], [-15, 15], color='r')
pl.plot([-10, 10], [20.0/3.0, -20.0/3.0], color='b')
pl.plot([-7, 13], [-15, 15], color='g')

pl.grid();
pl.xlim(-5, 5)
pl.ylim(-5, 5)

pl.annotate( r'$\vec{n_o} + [3, 0]$'
           , xy=(3.3, 0.34)
           , xytext=(10, -40)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='green', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="g")
)

pl.annotate( r'$\vec{n_o}\in \mathrm{N}(A)$'
           , xy=(2./12., 0.25)
           , xytext=(-30, 35)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='red', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="r")
)

pl.annotate( r'$[3, 0]$'
           , xy=(1.5, 0)
           , xytext=(-10, 35)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='cyan', shrink=0.05, connectionstyle="arc3,rad=0.1", fc="cyan")
)


pl.annotate( r'$\vec{r_0}\in\mathrm{C}(A^T)$'
           , xy=(0.7, -0.5)
           , xytext=(-30, -40)
           , textcoords='offset points'
           , fontsize='medium'
           , arrowprops=dict(facecolor='blue', shrink=0.05, connectionstyle="arc3,rad=-0.1", fc="b")
)

pl.show()

