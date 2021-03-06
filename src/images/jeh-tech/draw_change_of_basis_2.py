# Shameless rip of https://matplotlib.org/gallery/api/skewt.html
# and https://stackoverflow.com/questions/7761778/matplotlib-adding-second-axes-with-transparent-background
import matplotlib
from matplotlib.axes import Axes
import matplotlib.transforms as transforms
import matplotlib.axis as maxis
import matplotlib.spines as mspines
from matplotlib.projections import register_projection


# The sole purpose of this class is to look at the upper, lower, or total
# interval as appropriate and see what parts of the tick to draw, if any.
class SkewXTick(maxis.XTick):
    def update_position(self, loc):
        # This ensures that the new value of the location is set before
        # any other updates take place
        self._loc = loc
        super(SkewXTick, self).update_position(loc)

    def _has_default_loc(self):
        return self.get_loc() is None

    def _need_lower(self):
        return (self._has_default_loc() or
                transforms.interval_contains(self.axes.lower_xlim,
                                             self.get_loc()))

    def _need_upper(self):
        return (self._has_default_loc() or
                transforms.interval_contains(self.axes.upper_xlim,
                                             self.get_loc()))

    @property
    def gridOn(self):
        return (self._gridOn and (self._has_default_loc() or
                transforms.interval_contains(self.get_view_interval(),
                                             self.get_loc())))

    @gridOn.setter
    def gridOn(self, value):
        self._gridOn = value

    @property
    def tick1On(self):
        return self._tick1On and self._need_lower()

    @tick1On.setter
    def tick1On(self, value):
        self._tick1On = value

    @property
    def label1On(self):
        return self._label1On and self._need_lower()

    @label1On.setter
    def label1On(self, value):
        self._label1On = value

    @property
    def tick2On(self):
        return self._tick2On and self._need_upper()

    @tick2On.setter
    def tick2On(self, value):
        self._tick2On = value

    @property
    def label2On(self):
        return self._label2On and self._need_upper()

    @label2On.setter
    def label2On(self, value):
        self._label2On = value

    def get_view_interval(self):
        return self.axes.xaxis.get_view_interval()


# This class exists to provide two separate sets of intervals to the tick,
# as well as create instances of the custom tick
class SkewXAxis(maxis.XAxis):
    def _get_tick(self, major):
        return SkewXTick(self.axes, None, '', major=major)

    def get_view_interval(self):
        return self.axes.upper_xlim[0], self.axes.lower_xlim[1]


# This class exists to calculate the separate data range of the
# upper X-axis and draw the spine there. It also provides this range
# to the X-axis artist for ticking and gridlines
class SkewSpine(mspines.Spine):
    def _adjust_location(self):
        pts = self._path.vertices
        if self.spine_type == 'top':
            pts[:, 0] = self.axes.upper_xlim
        else:
            pts[:, 0] = self.axes.lower_xlim


# This class handles registration of the skew-xaxes as a projection as well
# as setting up the appropriate transformations. It also overrides standard
# spines and axes instances as appropriate.
class SkewXAxes(Axes):
    # The projection must specify a name.  This will be used be the
    # user to select the projection, i.e. ``subplot(111,
    # projection='skewx')``.
    name = 'skewx'

    def _init_axis(self):
        # Taken from Axes and modified to use our modified X-axis
        self.xaxis = SkewXAxis(self)
        self.spines['top'].register_axis(self.xaxis)
        self.spines['bottom'].register_axis(self.xaxis)
        self.yaxis = maxis.YAxis(self)
        self.spines['left'].register_axis(self.yaxis)
        self.spines['right'].register_axis(self.yaxis)

    def _gen_axes_spines(self):
        spines = {'top': SkewSpine.linear_spine(self, 'top'),
                  'bottom': mspines.Spine.linear_spine(self, 'bottom'),
                  'left': mspines.Spine.linear_spine(self, 'left'),
                  'right': mspines.Spine.linear_spine(self, 'right')}
        return spines

    def _set_lim_and_transforms(self):
        """
        This is called once when the plot is created to set up all the
        transforms for the data, text and grids.
        """
        rot = 45

        # Get the standard transform setup from the Axes base class
        Axes._set_lim_and_transforms(self)

        # Need to put the skew in the middle, after the scale and limits,
        # but before the transAxes. This way, the skew is done in Axes
        # coordinates thus performing the transform around the proper origin
        # We keep the pre-transAxes transform around for other users, like the
        # spines for finding bounds
        self.transDataToAxes = self.transScale + \
            self.transLimits + transforms.Affine2D().skew_deg(rot, 0)

        # Create the full transform from Data to Pixels
        self.transData = self.transDataToAxes + self.transAxes

        # Blended transforms like this need to have the skewing applied using
        # both axes, in axes coords like before.
        self._xaxis_transform = (transforms.blended_transform_factory(
            self.transScale + self.transLimits,
            transforms.IdentityTransform()) +
            transforms.Affine2D().skew_deg(rot, 0)) + self.transAxes

    @property
    def lower_xlim(self):
        return self.axes.viewLim.intervalx

    @property
    def upper_xlim(self):
        pts = [[0., 1.], [1., 1.]]
        return self.transDataToAxes.inverted().transform(pts)[:, 0]


# Now register the projection with matplotlib so the user can select
# it.
register_projection(SkewXAxes)

if __name__ == '__main__':
    # Now make a simple example using the custom projection.
    from matplotlib.ticker import (MultipleLocator, NullFormatter,
                                   ScalarFormatter)
    import matplotlib.pyplot as plt
    import numpy as np

    # Create a new figure. The dimensions here give a good aspect ratio
    fig = plt.figure()
    std_ax = fig.add_subplot(111)
    std_ax.grid(True)
 
    # std_ax.set_xticks([])
    # std_ax.set_yticks([])

    std_ax_pos = std_ax.get_position()
    print(std_ax_pos.x0, std_ax_pos.x1, std_ax_pos.y0, std_ax_pos.y1)
    print(std_ax_pos)
    cob_ax = fig.add_axes(std_ax_pos, frameon=False, projection='skewx')
    cob_ax.grid(True, color='red')
 


    axs = [std_ax, cob_ax]

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot
    for ax in axs:
        #break
        ax.plot([0,0], [0,1], lw=3)
        ax.plot([0,1], [0,0], lw=3)

        # ax.set_xlim([-1.25, 1.25])
        # ax.set_ylim([-1.25, 1.25])
    
    print(std_ax.get_xticks())
    print(cob_ax.get_xticks())

    ##
    ## TRY https://stackoverflow.com/questions/45037386/trouble-aligning-ticks-for-matplotlib-twinx-axes?noredirect=1&lq=1
    l = std_ax.get_xlim()
    l2 = cob_ax.get_xlim()
    f = lambda x : l2[0]+(x-l[0])/(l[1]-l[0])*(l2[1]-l2[0])
    ticks = f(std_ax.get_xticks())
    cob_ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(ticks))

    plt.show()
