import sys

from PySide import QtCore, QtGui

# IPython 4.x imports.
from ipykernel.inprocess.manager import InProcessKernelManager
from ipykernel.inprocess.ipkernel import InProcessInteractiveShell
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelClient


def create_kernel():
    kernel_manager = InProcessKernelManager()
    kernel_manager.start_kernel()
    kernel = kernel_manager.kernel
    kernel.gui = 'qt4'
    return kernel


def main():
    kernel = create_kernel()
    client1 = QtInProcessKernelClient(kernel=kernel)
    client1.session.key = kernel.session.key
    client1.start_channels()

    client2 = QtInProcessKernelClient(kernel=kernel)
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
