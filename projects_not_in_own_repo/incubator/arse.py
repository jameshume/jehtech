import matplotlib.pyplot as pl
import math

def rotate(x,y, degrees, tx, ty):
    rads = (math.pi/180.0) * degrees
    x -= tx
    y -= ty
    print(">", x, y)
    _x = x * math.cos(rads) - y * math.sin(rads)
    _y = y * math.cos(rads) + x * math.sin(rads)
    print(">", _x, _y)
    _x += tx
    _y += ty
    print(">", _x, _y)
    return (_x, _y)

TX = 10
TY = 10

x1, y1, x2, y2 = 16, 36, 16, 64

xr1, yr1 = rotate(x1, y1, 90, x1, y1)
xr2, yr2 = rotate(x2, y2, 90, x1, y1)

pl.plot([x1, x2], [y1, y2])
pl.plot([xr1, xr2], [yr1, yr2])
pl.show()