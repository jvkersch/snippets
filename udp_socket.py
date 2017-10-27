from __future__ import print_function
 
from PySide import QtNetwork
 
sock1 = QtNetwork.QUdpSocket()
sock2 = QtNetwork.QUdpSocket()
 
sock1.bind(QtNetwork.QHostAddress("127.0.0.1"), 8888)
sock2.bind(QtNetwork.QHostAddress("172.17.5.206"), 8888)
 
sock1.readyRead.connect(lambda: print("sock1"))
sock2.readyRead.connect(lambda: print("sock2"))
