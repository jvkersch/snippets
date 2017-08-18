import cPickle as pickle
import datetime
import json
import logging
import pprint
import sys

import numpy as np

from PySide import QtCore, QtGui
from qtconsole.client import QtKernelClient
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from jupyter_client import MultiKernelManager

logger = logging.getLogger(__name__)


def create_kernel_client(km):
    kid = km.start_kernel()
    kernel = km.get_kernel(kid)

    msg = 'Started new kernel {} (connection file {}, session key {})'
    logger.info(msg.format(kid, kernel.connection_file, kernel.session.key))

    # This is probably not the most optimal way to share connection data...
    with open(kernel.connection_file) as fp:
        connection = json.load(fp)
    logger.debug('Connection data:\n{}'.format(pprint.pformat(connection)))

    client = QtKernelClient(**connection)
    client.session.key = kernel.session.key
    client.start_channels()

    return client


def setup_environment(widget):
    # Send a mock dictionary of things to the kernel.
    data = {
        'x': np.array([1.0, 2.0, 3.0]),
        't': datetime.datetime.now()
    }
    pickled = pickle.dumps(data)
    message = (
        'import cPickle; globals().update(cPickle.loads({!r})); '
        'del cPickle'
    )
    formatted_msg = message.format(pickled)
    logger.debug('Sending environment string: {!r}'.format(formatted_msg))

    # Setting hidden=True (which is what we want to do) will trigger
    # https://github.com/jupyter/qtconsole/issues/68
    widget.execute(source=formatted_msg)  # , hidden=True)


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    vbox = QtGui.QVBoxLayout()

    manager = MultiKernelManager()

    client1 = create_kernel_client(manager)
    widget1 = RichJupyterWidget(buffer_size=10000)
    widget1.kernel_client = client1

    client2 = create_kernel_client(manager)
    widget2 = RichJupyterWidget(buffer_size=10000)
    widget2.kernel_client = client2

    vbox.addWidget(widget1)
    vbox.addWidget(widget2)

    button1 = QtGui.QPushButton("Set up #1")
    button1.clicked.connect(lambda: setup_environment(widget1))
    button2 = QtGui.QPushButton("Set up #2")
    button2.clicked.connect(lambda: setup_environment(widget2))

    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(button1)
    hbox.addWidget(button2)
    vbox.addLayout(hbox)

    window.setGeometry(QtCore.QRect(300, 300, 1000, 800))
    window.setWindowTitle('Two QT consoles connected to the same kernel')
    window.setLayout(vbox)
    window.show()
    window.activateWindow()
    window.raise_()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
