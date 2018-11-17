

# You're not actually adding a new axes.

# Matplotlib is detecting that there's already a plot in that position and returning it instead of a new axes 
# object.

# (Check it for yourself. ax and newax will be the same object.)

# There's probably not a reason why you'd want to, but here's how you'd do it.

# (Also, don't call newax = plt.axes() and then call fig.add_subplot(newax) You're doing the same thing twice.)

# Edit: With newer (>=1.2, I think?) versions of matplotlib, you can accomplish the same thing as the 
# example below by using the label kwarg to fig.add_subplot. 
# E.g. newax = fig.add_subplot(111, label='some unique string')

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.grid(True)
# If you just call `plt.axes()` or equivalently `fig.add_subplot()` matplotlib  
# will just return `ax` again. It _won't_ create a new axis unless we
# call fig.add_axes() or reset fig._seen
newax = fig.add_axes(ax.get_position(), frameon=False)
newax.grid(True)
ax.plot(range(10), 'r-')
newax.plot(range(50), 'g-')
newax.axis('equal')

plt.show()