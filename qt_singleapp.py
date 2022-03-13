import sys


from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtCore import QObject, QByteArray


class Single(QObject):
    
    def __init__(self):
        super().__init__()

    def isRunning(self):
        localSocket = QLocalSocket()
        localSocket.connectToServer("HamMessenger2-Server")
        hey = QByteArray()
        if localSocket.write(hey) < 0:
            ret = False
        else:
            ret = True
        localSocket.abort()
        return ret


    def startServer(self):   
        self.server = QLocalServer(self)
        self.server.listen("HamMessenger2-Server")
        self.server.newConnection.connect(self.reply)

    def reply(self):
        pass

    def serverClose(self):
        self.server.close()


