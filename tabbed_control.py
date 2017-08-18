"""
Simple example of controlling the tab that's shown in a Tabbed via
an external event (e.g. Button). This came up in a Genia-related question.

This is also an example for myself of a minimal tasks application.

"""

from collections import deque

from pyface.api import GUI
from pyface.tasks.api import Task, TraitsEditor, TaskWindow
from pyface.tasks.i_advanced_editor_area_pane import IAdvancedEditorAreaPane
from pyface.tasks.advanced_editor_area_pane import AdvancedEditorAreaPane
from traits.api import Button, Instance, Str
from traitsui.api import Tabbed, UItem, VGroup, View

from PySide.QtGui import QTabWidget


class A(TraitsEditor):

    foo = Str('foo')
    bar = Str('bar')
    baz = Str('baz')

    advance = Button('Advance')

    def default_traits_view(self):
        view = View(
            VGroup(
                Tabbed(
                    UItem('foo', style='readonly'),
                    UItem('bar', style='readonly'),
                    UItem('baz', style='readonly'),
                ),
                UItem('advance')
            )
        )
        return view

    def _advance_changed(self):
        # BFS to find QTabWidget closest to the top of the hierarchy.
        children = deque(self.control.children())
        tab_widget = None
        while children:
            child = children.popleft()
            if isinstance(child, QTabWidget):
                tab_widget = child
                break
            children.extend(child.children())

        if tab_widget is None:
            print "Couldn't find tab widget"
            return
        # tab_widget = self.control.children()[1]
        index = tab_widget.currentIndex()
        if index != -1:
            tab_widget.setCurrentIndex((index + 1) % tab_widget.count())

    @classmethod
    def from_model(cls, editor_area, obj):
        return cls()


class MyTask(Task):

    editor_area = Instance(IAdvancedEditorAreaPane)

    def edit(self, obj, factory=None, use_existing=True):
        editor = self.editor_area.create_editor(obj, factory)
        self.editor_area.add_editor(editor)
        self.editor_area.activate_editor(editor)

    def create_central_pane(self):
        self.editor_area = AdvancedEditorAreaPane()
        return self.editor_area


if __name__ == '__main__':
    task = MyTask()
    gui = GUI()
    window = TaskWindow(size=(300, 300))
    task.create_central_pane()
    window.add_task(task)
    task.edit(None, A.from_model)
    window.open()
    gui.start_event_loop()
