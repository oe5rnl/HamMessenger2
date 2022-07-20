
#import simpleaudio as sa
from PyQt5.QtCore import QThread, QObject

class Player(QObject):

    def __init__(self):
        super().__init__()


    def play(self,file):
 
        # self.threadPlay = QThread(parent=self)
        # self._play = Play()
        # self._play.setFile(file)
        # self._play.moveToThread(self.threadPlay)
        # self.threadPlay.started.connect(self._play.run)  
        # self.threadPlay.start()
        pass


class Play(QObject):
    
    def __init__(self):
        super().__init__()

    def setFile(self,file):
        self.file=file

    def run(self):
        # w = sa.WaveObject.from_wave_file(self.file)
        # p = w.play()
        # p.wait_done()
        pass

