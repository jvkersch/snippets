from traits.api import Bool, Enum, HasTraits, Int
from traitsui.api import Controller, OKCancelButtons, View


class ExampleModel(HasTraits):

    x = Int(42)
    enum = Enum('foo', 'bar', 'baz')


example_view = View('x', 'enum', buttons=OKCancelButtons, title='my app')


class ExampleController(Controller):

    dirty = Bool(False)

    def apply(self, info):
        print 'Running apply with info:', info
        return super(ExampleModel, self).apply(info)

    def object_x_changed(self, info):
        if info.initialized:
            if not self.dirty:
                info.ui.title += '*'
                self.dirty = True


if __name__ == '__main__':
    m = ExampleModel()
    m.configure_traits(view=example_view, handler=ExampleController())
