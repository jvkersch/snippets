"""
Experimentation with setting the selected range on a range tool.

This came out of some confusion of mine where I tried to set the "selected"
trait on a range tool before the plot (with the range overlay) had been
rendered on the screen).  This caused the overlay and the tool to come up in an
inconsistent state.

Setting the "selected" trait after the plot has displayed works perfectly.

"""

from enable.api import Component, ComponentEditor
from traits.api import HasStrictTraits, Instance, Any, Button
from traitsui.api import UItem, View, VGroup
from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import RangeSelection, RangeSelectionOverlay

import numpy as np


class Demo(HasStrictTraits):
    range_tool = Any
    select = Button("Select")

    view = View(
        VGroup(
            UItem('plot', editor=ComponentEditor()),
            UItem('select')
        )
    )
    plot = Instance(Component)

    def _plot_default(self):
        plot_data = ArrayPlotData(
            x=np.linspace(0, 1, 10), y=np.linspace(0, 1, 10)
        )
        plot = Plot(plot_data)
        r, = plot.plot(("x", "y"))
        range_tool = RangeSelection(r)
        r.overlays.append(RangeSelectionOverlay(axis='index', component=r))
        r.tools.append(range_tool)
        self.range_tool = range_tool
        return plot

    def _select_changed(self):
        self.range_tool.selection = (0.2, 0.4)


if __name__ == '__main__':
    Demo().configure_traits()
