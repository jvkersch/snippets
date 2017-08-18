
from traits.api import Enum, HasTraits, Str, Int, List, Property, Instance, on_trait_change
from traitsui.api import Controller, TableEditor, ObjectColumn,View, Item, HGroup


class Foo(HasTraits):

    trait_1 = Str('Foo', column_trait=True)

    trait_2 = Int(column_trait=True)


class Bar(HasTraits):

    trait_1 = Str('Bar', column_trait=True)

    trait_3 = Int(column_trait=True)

    trait_4 = Int  # no metadata, so don't display


class FooBarList(HasTraits):

    foos_or_bars = Enum('foo', 'bar', 'both')

    foobars = List

    def __init__(self, **traits):
        super(FooBarList, self).__init__(**traits)
        self.update_foobars()

    def _foos_or_bars_changed(self):
        self.update_foobars()

    def update_foobars(self):
        if self.foos_or_bars == 'foo':
            self.foobars = [Foo(trait_2=i) for i in range(10)]
        elif self.foos_or_bars == 'bar':
            self.foobars = [Bar(trait_3=10+i**2) for i in range(10)]
        else:
            self.foobars = [Foo(trait_2=i) for i in range(5)] + \
                [Bar(trait_3=10+i**2) for i in range(5)]


class FooBarListController(Controller):

    model = Instance(FooBarList)

    def init(self, info):
        # set up inital columns, could also do this with a more dynamic view
        self.update_columns()

    @on_trait_change('model.foobars,model.foobars_items')
    def update_columns(self):
        if self.info is not None:
            # only compute if we have a UI up and running
            column_names = set()
            for foobar in self.model.foobars:
                print foobar
                column_names |= set(foobar.trait_names(column_trait=True))
            columns = [ObjectColumn(name=name) for name in sorted(column_names)]
            editor = self.info.ui.get_editors('foobars')[0]
            editor.columns = columns

    view = View(
        HGroup(Item('foos_or_bars')),
        Item(
            'foobars',
            show_label=False,
            editor=TableEditor(
            )
        ),
        resizable=True,
    )


if __name__ == '__main__':
    model = FooBarList()
    controller = FooBarListController(model=model)
    controller.configure_traits()
