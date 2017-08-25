from pyface.api import GUI
from pyface.tasks.api import TaskWindow, Task, TraitsTaskPane
from traitsui.api import Label, View


class MyCentralPane(TraitsTaskPane):
    id = "mypane"
    name = "My Pane"

    view = View(Label("Central Pane"))


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
