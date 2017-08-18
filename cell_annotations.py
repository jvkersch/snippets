from traits.api import Button, Callable, Dict, HasStrictTraits, Instance, List, Property, Unicode, cached_property
from traitsui.api import (
    OKCancelButtons, SetEditor, TabularEditor, UItem, VGroup, View
)
from traitsui.tabular_adapter import TabularAdapter

DATA = [('A', 1), ('B', 2), ('D', 4), ('C', 3)]


class CellAdapter(TabularAdapter):

    columns = [u'Name', u'Value']


class Selector(HasStrictTraits):
    """ Modal dialog to select a number of elements from a set.

    The user provides a list of items to select from in the `all_items` trait,
    a list of currently selected items in `selected_items`, and calls `show()`
    to bring up a selection dialog. After the user has completed the
    interaction with the dialog, the new selection is in `selected_items`.

    """

    # Public api ##############################################################

    #: Title of the dialog.
    title = Unicode

    #: The collection of all items to select from.
    all_items = List

    #: The currently selected items.
    selected_items = List

    #: A callable to turn selection items into a string representation shown in
    #: the selection window. This must take one argument (the item) and return
    #: a (unicode) string.
    formatter = Callable

    def show(self):
        """ Pop up dialog window.
        """
        self.edit_traits(kind='modal')

    # Private api #############################################################

    #: Names of the selected items, obtained by applying self.formatter to the
    #: elements of self.selected_items .
    _selected_items_names = Property(List(Unicode))

    #: Lookup table mapping item names to items.
    _all_items_lut = Property(Dict, depends_on='all_items, formatter')

    #: Names of all items.
    _all_items_names = Property(List(Unicode), depends_on='_all_items_lut')

    def default_traits_view(self):
        view = View(
            VGroup(
                UItem('_selected_items_names', editor=SetEditor(
                    name='_all_items_names',
                    ordered=True,
                    left_column_title=u'Not Displayed',
                    right_column_title=u'Displayed')
                ),
            ),
            title=self.title,
            buttons=OKCancelButtons
        )
        return view

    def _formatter_default(self):
        return str

    @cached_property
    def _get__all_items_lut(self):
        return {
            self.formatter(item): item for item in self.all_items
        }

    @cached_property
    def _get__all_items_names(self):
        return sorted(self._all_items_lut.keys())

    def _get__selected_items_names(self):
        return [self.formatter(item) for item in self.selected_items]

    def _set__selected_items_names(self, value):
        self.selected_items = [self._all_items_lut[name] for name in value]


class CellAnnotationViewer(HasStrictTraits):

    all_records = List

    selected_records = List

    select_annotations = Button('Select Annotations...')

    view = View(
        VGroup(
            UItem('selected_records', editor=TabularEditor(
                adapter=CellAdapter(),
                operations=[],
                editable=False,
                auto_resize=False,
                auto_resize_rows=True)
            ),
            UItem('select_annotations')
        )
    )

    def _selected_records_default(self):
        return sorted(self.all_records)

    def _select_annotations_changed(self):
        selector = Selector(
            title='Select Annotations',
            all_items=self.all_records,
            selected_items=self.selected_records,
            formatter=lambda (name, _): name
        )
        selector.show()
        self.selected_records = sorted(selector.selected_items)


if __name__  == '__main__':
    viewer = CellAnnotationViewer(
        all_records=DATA
    )
    viewer.configure_traits()
