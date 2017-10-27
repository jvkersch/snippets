from functools import partial

from pyface.api import GUI
from pyface.tasks.api import TaskWindow, Task, TraitsTaskPane
from traitsui.api import Label, View, UItem
from traits.api import Any, Enum, Code, List, HasStrictTraits

from pyface.qt import QtGui, QtCore


class ShortcutDispatcher(HasStrictTraits):

    shortcut_keys = List(list("abcdef"))
    control = Any

    def __init__(self, control):
        self.control = control
        for key in self.shortcut_keys:
            self._make_shortcut(key)

    def _make_shortcut(self, key):
        print("making shortcut for {}".format(key))
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(key), self.control)
        shortcut.setContext(QtCore.Qt.ApplicationShortcut)
        shortcut.activated.connect(partial(self._dispatch, key=key))

    def _dispatch(self, key):
        print("key {} pressed".format(key))


class MyCentralPane(TraitsTaskPane):
    id = "mypane"
    name = "My Pane"

    keys = Enum(list("abcdefgh"))

    code = Code
    
    view = View(
        UItem('code', style='custom', resizable=True),
        UItem('keys')
    )
    
    shortcut = Any
    dispatcher = Any

    def create(self, parent):
        super(MyCentralPane, self).create(parent)
        # shortcut = QtGui.QShortcut(QtGui.QKeySequence("a"), self.control)
        # shortcut.setContext(QtCore.Qt.ApplicationShortcut)
        # shortcut.activated.connect(self._print_key_message)
        # self.shortcut = shortcut
        self.dispatcher = ShortcutDispatcher(self.control)



class MyTask(Task):
    id = "mytask"
    name = "My Task"

    def create_central_pane(self):
        return MyCentralPane()


if __name__ == '__main__':
    gui = GUI()
    window = TaskWindow(size=(400, 300))
    window.add_task(MyTask())
    window.open()
    gui.start_event_loop()
