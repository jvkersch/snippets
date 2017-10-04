"""
Simple example of a stacked bar chart

Modified by Connor Lynch for updates to bar plot.  Modified by jvkersch to show
tick labels on the horizontal axis for each bar.

"""

# Major library imports
import numpy
import numpy as np

# Enthought library imports
from enable.api import ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import UItem, View

# Chaco imports
from chaco.api import LabelAxis, Plot, ArrayPlotData, PlotAxis
from chaco.ticks import ShowAllTickGenerator


from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, View

from chaco.api import (
    ArrayDataSource, BarPlot, DataRange1D, LabelAxis,
    LinearMapper, OverlayPlotContainer, PlotAxis, Legend
)
from chaco.tools.api import (
    PanTool, LegendTool, BroadcasterTool
)


class PlotExample(HasTraits):
    plot = Instance(Plot)
    traits_view = View(UItem('plot', editor=ComponentEditor()),
                       width=400, height=400, resizable=True, 
                      )

    def __init__(self, index, series_a, series_b, series_c, **kw):
        super(PlotExample, self).__init__(**kw)

        plot_data = ArrayPlotData(index=index)
        starting_values = np.ones(10) * 0.5
        starting_vals = ArrayDataSource(starting_values,
                                        sort_order="none")
        series_a = series_a + starting_values
        plot_data.set_data('series_a', series_a)
        plot_data.set_data('series_b', series_b)
        plot_data.set_data('series_c', series_c)
        self.plot = Plot(plot_data)

        self.plot.plot(('index', 'series_a'), type='bar', bar_width=0.8, color='auto', starting_value=starting_vals)

        # set the plot's value range to 0, otherwise it may pad too much
        self.plot.value_range.low = 0

        tick_positions_and_labels = {
            x: 'label_{}'.format(x) for x in range(1, 11)
        }
        tick_generator = ShowAllTickGenerator(
            positions=tick_positions_and_labels.keys()
        )

        def formatter(value):
            return tick_positions_and_labels[int(value)]

        plot_axis = PlotAxis(
            component=self.plot,
            mapper=self.plot.x_mapper,
            # labels=labels,
            orientation='bottom',
            tick_generator=tick_generator,
            tick_label_rotate_angle=-45.,
            tick_label_alignment='corner',
            tick_label_formatter=formatter,
            tick_label_offset=3
        )


        self.plot.underlays.remove(self.plot.index_axis)
        self.plot.index_axis = plot_axis
        self.plot.overlays.append(plot_axis)


index = np.arange(1, 11)
default_vals = np.ones(10)
demo = PlotExample(index, default_vals*1, default_vals*2, default_vals*3)

if __name__ == "__main__":
    demo.configure_traits()




