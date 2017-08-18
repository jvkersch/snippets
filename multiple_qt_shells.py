import logging
import sys

from PySide import QtCore, QtGui

from traitlets import Instance
from ipykernel.inprocess.manager import InProcessKernelManager
from ipykernel.inprocess.ipkernel import InProcessKernel
from ipykernel.comm import CommManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelClient


class ShellableInProcessKernel(InProcessKernel):

    def __init__(self, *args, **kwargs):
        # We want to skip the initialization of the parent class, which sets up
        # the shell, as we'll set up the shell manually via create_shell().
        # super(InProcessKernel, self).__init__(*args, **kwargs)
        # self.comm_manager_registry = {}
        # self.shell_registry = {}

        super(ShellableInProcessKernel, self).__init__(*args, **kwargs)
        self.comm_manager_registry = {
            id(self.shell): self.comm_manager
        }
        self.shell_registry = {
            id(self.shell): self.shell
        }

    def _shell_changed(self, name, old, new):
        print '*** Changing shell ***'

    def create_shell(self):
        shell = self.shell_class.instance(
            parent=self,
            profile_dir=self.profile_dir,
            user_module=self.user_module,
            user_ns=self.user_ns,
            kernel=self,
        )
        comm_manager = CommManager(
            shell=shell, parent=self, kernel=self
        )
        shell.configurables.append(comm_manager)

        self.shell_registry[id(shell)] = shell
        self.comm_manager_registry[id(shell)] = comm_manager

        return shell, comm_manager

    def connect_shell(self, shell):
        print 'Connecting shell {}'.format(id(shell))
        
        old_shell = self.shell
        print 'Disconnecting shell {}'.format(id(old_shell))
        self._disconnect(old_shell)

        
        # Set shell and connect everything
        self.shell = shell
        self.shell.displayhook.session = self.session
        self.shell.displayhook.pub_socket = self.iopub_socket
        self.shell.displayhook.topic = self._topic('execute_result')
        self.shell.display_pub.session = self.session
        self.shell.display_pub.pub_socket = self.iopub_socket
        self.shell.data_pub.session = self.session
        self.shell.data_pub.pub_socket = self.iopub_socket

        self.shell._reply_content = None

        comm_manager = self.comm_manager_registry[id(shell)]
        self.comm_manager = comm_manager

        comm_msg_types = ['comm_open', 'comm_msg', 'comm_close']
        for msg_type in comm_msg_types:
            self.shell_handlers[msg_type] = getattr(comm_manager, msg_type)

    def _disconnect(self, old_shell):
        old_shell.displayhook.session = None
        old_shell.displayhook.pub_socket = None
        old_shell.display_pub.session = None
        old_shell.display_pub.pub_socket = None
        old_shell.data_pub.session = None
        old_shell.data_pub.pub_socket = None


class ShellableInProcessKernelManager(InProcessKernelManager):

    def start_kernel(self, **kwds):
        self.kernel = ShellableInProcessKernel(
            parent=self, session=self.session
        )


class ShellableQtInProcessKernelClient(QtInProcessKernelClient):

    shell = Instance('ipykernel.zmqshell.ZMQInteractiveShell')

    def _dispatch_to_kernel(self, *args, **kwargs):
        # TODO This disconnects the old shell and reconnects a new one every
        # time a message is sent to the kernel. Better would be to do this
        # switching around only when the client becomes "active" (e.g. when the
        # widget gains focus)
        print 'Switch over to shell {}'.format(id(self.shell))
        self.kernel.connect_shell(self.shell)
        return super(ShellableQtInProcessKernelClient, self)\
            ._dispatch_to_kernel(*args, **kwargs)


def create_kernel():
    kernel_manager = ShellableInProcessKernelManager()
    kernel_manager.start_kernel()
    kernel = kernel_manager.kernel
    kernel.gui = 'qt4'
    return kernel


def main():
    # logging.basicConfig(level=logging.DEBUG)

    kernel = create_kernel()

    client1 = ShellableQtInProcessKernelClient(kernel=kernel)
    client1.shell = kernel.shell
    client1.session.key = kernel.session.key
    client1.start_channels()

    # Create another shell and a client to drive it
    shell, _ = kernel.create_shell()
    client2 = QtInProcessKernelClient(kernel=kernel)
    client2.shell = shell
    client2.session.key = kernel.session.key
    client2.start_channels()

    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    vbox = QtGui.QVBoxLayout()

    widget1 = RichJupyterWidget(buffer_size=10000)
    widget1.kernel_client = client1
    vbox.addWidget(widget1)

    widget2 = RichJupyterWidget(buffer_size=10000)
    widget2.kernel_client = client2
    vbox.addWidget(widget2)

    window.setGeometry(QtCore.QRect(300, 300, 1000, 800))
    window.setWindowTitle('Two QT consoles connected to the same kernel')
    window.setLayout(vbox)
    window.show()
    window.activateWindow()
    window.raise_()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
