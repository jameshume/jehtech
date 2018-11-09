import numpy as np
import mayavi.mlab as m

p0 = [0.799319, -3.477045e-01, 0.490093]
p1 = [0.852512, 9.113778e-16, -0.522708]
p2 = [0.296422, 9.376042e-01, 0.181748]

origin = [0,0,0]
X, Y, Z = zip(origin,origin,origin) 
U, V, W = zip(p0,p1,p2)

m.quiver3d(X,Y,Z,U,V,W)
