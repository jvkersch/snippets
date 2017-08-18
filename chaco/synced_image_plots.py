import numpy as np

from chaco.api import ArrayPlotData, GridPlotContainer, Plot
from chaco.tools.api import PanTool, ZoomTool
from enable.api import ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, View


def add_tools(renderer):
    pt = PanTool(renderer)
    zt = ZoomTool(renderer)
    renderer.tools.extend([pt, zt])


def share_attr(objs, name):
    if not objs:
        return
    attr = getattr(objs[0], name)
    for obj in objs[1:]:
        setattr(obj, name, attr)


class GridContainerExample(HasTraits):

    plot = Instance(GridPlotContainer)

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=1000, height=600, resizable=True
    )

    def _plot_default(self):
        # Create a GridContainer to hold all of our plots: 2 rows, 3 columns
        container = GridPlotContainer(shape=(2, 3),
                                      spacing=(10, 5),
                                      valign='top',
                                      bgcolor='lightgray')

        pd = ArrayPlotData(data=np.arange(36).reshape(6, 6))

        plots = []
        renderers = []
        for i in range(6):
            plot = Plot(pd)
            r, = plot.img_plot("data")

            plots.append(plot)
            renderers.append(r)
            add_tools(r)

            # Add to the grid container
            container.add(plot)

        share_attr(plots, "range2d")
        share_attr(
            [rend.index_mapper for rend in renderers], "range"
        )   
        return container


if __name__ == "__main__":
    GridContainerExample().configure_traits()
