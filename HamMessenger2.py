#!/usr/bin/python3

#---------------------------------------------------------------------------------------------------------------
#  filename: server_connector.py
#  date: 2022-06-03
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3
#
#  based on     HamMessenger old base 1.5.4  14.05.2018  protocol 1
# 
# ===========================================================================
#
# pyuic5 -x main.ui -o main-ui.py
#

import sys
#import traceback
import time
import datetime
from os.path import exists

from xml.etree.ElementTree import Comment

from PyQt5.QtWidgets import (QMessageBox, QSplashScreen)

from PyQt5.uic import *

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer, QEvent
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

import com
import qt_config
import qt_group
import server_connector
import qt_online
import qt_guimode
import qt_history
import qt_msglog

import qt_player

import logging
import get_OS
import qt_singleapp


logger = logging.getLogger(__name__)


logging.basicConfig(filename=get_OS.getUserDataPath()+'HamMessenger2_DEBUG.log', filemode='a', level=logging.DEBUG)

def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    """Handler for unhandled exceptions that will write to the logs"""
    if issubclass(exc_type, KeyboardInterrupt):
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

#sys.excepthook = handle_unhandled_exception


class Main(QObject):

    def __init__(self):
        super().__init__()
 
        #start = time.time()

        self.msg_i = 1

        if get_OS.isOsWindows():
            import ctypes
            myappid = 'HamRadio.Communication.HamMessanger.0.55' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.cs = True
        self.cs_old = True

        self.app = QtWidgets.QApplication(sys.argv)

        self.singleApp = qt_singleapp.Single()
        if self.singleApp.isRunning():
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("HamMessenger2 is still runnig")
            msgBox.setWindowTitle("HamMessenger2")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            exit(0)
        else:
            self.singleApp.startServer()
 
        self.flashSplash()

        self.app.setWindowIcon(QtGui.QIcon(get_OS.getUserDataPath()+"res/worldwide.png"))   

        self.ui = loadUi(get_OS.getAPPPath()+"main.ui")
        self.ui.setWindowIcon(QtGui.QIcon(get_OS.getUserDataPath()+"res/worldwide.png"))   
        self.ui.labelVersion.setText('Ham Messenger - Version: '+com.date+' '+com.version)
        self.ui.comboBoxGuiStyle.addItems(['dark','light'])
        pixmap = QPixmap(get_OS.getUserDataPath()+"res/Raute_klein.jpg")
        self.ui.labelRaute.setPixmap(pixmap)

        self.config = qt_config.Config(self.ui)
 
        self.player = qt_player.Player()
        self.config.testTone_emit.connect(self.on_testTone)

        self.ui.resize(int(self.config.mainWSize.split(',')[0]),
                       int(self.config.mainWSize.split(',')[1]))

        self.guimode = qt_guimode.GuiMode(self.app,self.config )
        self.config.guimode_emit.connect(self.on_guimode)
    
        self.groupList = qt_group.GroupDialog(self.ui,self.config)

        self.ui.pushButtonBC.clicked.connect(self.on_pushButtonBC)
        self.ui.pushButtonCQ.clicked.connect(self.on_pushButtonCQ)
        self.ui.pushButtonGC.clicked.connect(self.on_pushButtonGC)
        self.ui.pushButtonPC.clicked.connect(self.on_pushButtonPC)
        self.ui.pushButtonEC.clicked.connect(self.on_pushButtonEC)

        self.ui.textEditBC.textChanged.connect(lambda: self.txtInputChanged(self.ui.textEditBC))
        self.ui.textEditCQ.textChanged.connect(lambda: self.txtInputChanged(self.ui.textEditCQ))
        self.ui.textEditGC.textChanged.connect(lambda: self.txtInputChanged(self.ui.textEditGC))
        self.ui.textEditPC.textChanged.connect(lambda: self.txtInputChanged(self.ui.textEditPC))
        self.ui.textEditEC.textChanged.connect(lambda: self.txtInputChanged(self.ui.textEditEC))

        KeyHelper(self.ui.textEditBC).keyPressed.connect(self.onEnterTextEditBC)
        KeyHelper(self.ui.textEditCQ).keyPressed.connect(self.onEnterTextEditCQ)
        KeyHelper(self.ui.textEditGC).keyPressed.connect(self.onEnterTextEditGC)
        KeyHelper(self.ui.textEditPC).keyPressed.connect(self.onEnterTextEditPC)
        KeyHelper(self.ui.textEditEC).keyPressed.connect(self.onEnterTextEditEC)

        self.set_StatusLine(mode='con')

        self.online = qt_online.OnlineTableView(self.ui,self.config)
        self.ui.tableViewOnline.doubleClicked.connect(self.on_rowClickOnline)

        self.history = qt_history.History(self.ui,self.guimode,self.config)
        self.ui.tableWidgetHistory.doubleClicked.connect(self.on_rowClickHistory)


        self.tableWidgetLog = qt_msglog.TableWidgetLog(self.ui)
     

        self.ui.comboBoxPrivateCalls.addItem('please select call')
        self.online.model.calls_changed.connect(self.addPrivateCalls)

        self.threadClock = QThread(parent=self)
        self.clock = Clock()
        self.clock.moveToThread(self.threadClock)
        self.threadClock.started.connect(self.clock.run)  
        self.clock.tick.connect(self.on_ClockTick)           
        self.threadClock.start()

        self.app_server_connector = server_connector.Server(self.config)
        self.config.addServer(self.app_server_connector)
  
        self.app_server_connector.rx.online_emit.connect(self.on_online)
        self.app_server_connector.rx.msg_emit.connect(self.on_msg)
        self.app_server_connector.rx.close_emit.connect(self.on_close)
 
        self.send = server_connector.Send(self.config)

        if len(self.config.call.strip())>0:
            self.app_server_connector.reconnect()

        self.app_server_connector.start() 
        self.config.save_emit.connect(self.a) #self.send.HB)
        self.send.HB()

        self.app.aboutToQuit.connect(self.closeEvent)

        self.ui.show()

        ende = time.time()
        #print('{:5.3f}s'.format(ende-start))


        self.app.exec_()
        # --- end main-init ---

    def a(self):
        #print('*hb1')
        self.send.HB()
        #print('*hb2')
        


    def on_rowClickOnline(self, mi):
        row = mi.row()
        self.ui.tabWidgetMessages.setCurrentIndex(3)
        self.setPrivateCall(self.online.getCall(row))

    def on_rowClickHistory(self, mi):
        row = mi.row()
        self.ui.tabWidgetMessages.setCurrentIndex(3)
        self.setPrivateCall(self.history.getCall(row))


    def onEnterTextEditBC(self,key):
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and self.config.sendbyenter:
            self.on_pushButtonBC()

    def onEnterTextEditCQ(self,key):
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_pushButtonCQ()

    def onEnterTextEditGC(self,key):
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_pushButtonGC()

    def onEnterTextEditPC(self,key):
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_pushButtonPC()

    def onEnterTextEditEC(self,key):
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_pushButtonEC()



    def flashSplash(self):
        self.splash = QSplashScreen(QPixmap(get_OS.getUserDataPath()+"res/Raute_klein.jpg"))
        # self.splash.move(10,10)
        self.splash.show()

        # Close SplashScreen after 2 seconds (2000 ms)
        QTimer.singleShot(2000, self.splash.close)

    def on_testTone(self):
        self.player.play(get_OS.getUserDataPath()+"/res/buzzer_x.wav")


    def on_close(self,emsg):
        self.online.closeCall(emsg)

    def addPrivateCalls(self,calls):
   
        akt_call = self.ui.comboBoxPrivateCalls.currentText()
        self.ui.comboBoxPrivateCalls.clear()
        self.ui.comboBoxPrivateCalls.addItem('please select call')
        self.ui.comboBoxPrivateCalls.addItems(calls)
        index = self.ui.comboBoxPrivateCalls.findText(akt_call, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.ui.comboBoxPrivateCalls.setCurrentIndex(index)

    def setPrivateCall(self,call):
        index = self.ui.comboBoxPrivateCalls.findText(call, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.ui.comboBoxPrivateCalls.setCurrentIndex(index)

    def on_guimode(self,mode): 
        self.guimode.setGuiMode(mode)

    def on_msg(self,emsg):
        self.history.append(emsg)
        self.tableWidgetLog.append2Log(emsg)

        if self.ui.checkBoxAlertTone.isChecked():
            if emsg['PayloadTypeString'] == 'EM':
                self.player.play(get_OS.getUserDataPath()+"/res/buzzer_x.wav")
            else:
                self.player.play(get_OS.getUserDataPath()+"/res/hinweis.wav")

    def on_online(self,emsg):
        self.online.append(emsg)

    def txtInputChanged(self,textEdit):
        # ACHTUNG: Keinen längeren text senden.
        if len(textEdit.toPlainText()) > 300:
            text = textEdit.toPlainText()
            text = text[:300]
            textEdit.setPlainText(text)
            cursor = textEdit.textCursor()
            cursor.setPosition(300)
            textEdit.setTextCursor(cursor)

    def on_pushButtonBC(self):

        if self.checkCallName():
            txt = self.ui.textEditBC.toPlainText().strip()
            if len(txt) > 0:
                self.send.BC(txt)
                self.ui.textEditBC.clear() #.setText('')
            else:
                self.needTextDialog('Send Broadcast')    

    def on_pushButtonCQ(self):

            if self.checkCallName():
                txt = self.ui.textEditCQ.toPlainText().strip()
            if len(txt) > 0:
                self.send.CQ(txt)
                self.ui.textEditCQ.clear() #.setText('')              
            else:
                self.needTextDialog('Send CQ') 

    def on_pushButtonGC(self):
        if self.checkCallName():
            txt = self.ui.textEditGC.toPlainText().strip()
            if len(txt) > 0:
                
                group = self.groupList.getGroup()
                if self.groupList.isValidGroup(group):
                    self.send.GC(group,txt)
                    self.ui.textEditGC.clear() #.setText('')
                    pass
                else:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText("select valid group")
                    msgBox.setWindowTitle("select valid group")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()
            else:
                self.needTextDialog('Send Group Call') 

    def on_pushButtonPC(self):
        if self.checkCallName():
            txt = self.ui.textEditPC.toPlainText().strip()
            if len(txt) > 0:
                call = self.ui.comboBoxPrivateCalls.currentText()
                self.send.PC(call,txt)
                self.ui.textEditPC.clear() 
            else:
                self.needTextDialog('Send Personal Call')    


    def on_pushButtonEC(self):
        if self.checkCallName():
            txt = self.ui.textEditEC.toPlainText().strip()
            if len(txt) > 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Are you shure to send this Emergency Message\n"+txt)
                msgBox.setWindowTitle('Send Emergency call')
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)     
                returnValue = msgBox.exec() 
                if returnValue == QMessageBox.Ok:
                    self.send.EC(txt)
                    self.ui.textEditEC.clear() #.setText('')
                pass
            else:
                self.needTextDialog('Emergency Broadcast')    


    def needTextDialog(self,title):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Text needed")
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)     
        msgBox.exec() 

    def checkCallName(self):

        if (  self.config.call=='your call' or len(self.config.call.strip())==0 
           or self.config.name=='your name' or len(self.config.name.strip())==0 
          ):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("no call or name, check Setup!")
            msgBox.setWindowTitle("Config Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return False
        else:
            return True

    def closeEvent(self):
        self.exitFunction()
 
    def exitFunction(self):
        self.send.CLOSE()
        time.sleep(1)
        self.clock.stop()    
        self.threadClock.quit()
        self.app_server_connector.stop()    
        self.config.mainWSize = str(self.ui.width())+','+str(self.ui.height())            
        self.config.write_config()
        time.sleep(2)  
        self.singleApp.serverClose()
        sys.exit()

    def on_ClockTick(self,dt):

        self.ui.setWindowTitle("HAM-Messanger2 by OE5RNL & OE5NVL ("+com.version+") based on OE1KBCs .NET Client   -   "+dt+"")
        if ((int(time.strftime("%S")) % 5)==0):
            self.cs_old = self.cs
            if len(self.config.call.strip())>0:
                self.cs = self.app_server_connector.reconnect()
                self.set_StatusLine(cs=self.cs)

                if self.cs_old and not self.cs:
                    self.app_server_connector.rx.errorMsg('er','--','--','Connection to the HAMGO module not possible.\nHAMGO Module offline or check Setup please')
                if not self.cs_old and self.cs:
                    self.app_server_connector.rx.errorMsg('ok','--','--','Reconnect to the HAMGO Module done')
            else:
                self.set_StatusLine(cs=False)


    def set_StatusLine(self,cs=False,mode=''):

        if self.config.call=='':
            txt = 'Please set call, name, qth, locator etc in tab Setup '
        else:
            txt = '  '+self.config.call+' '+self.config.name+' '+self.config.qth+' '+self.config.locator+'  '
        if mode=='con':
            self.ui.labelStatus.setStyleSheet("background:QColor(253,17,63);")
            self.ui.labelStatus.setText(txt+'(Connecting...)')
        else:
            if cs:    
                self.ui.labelStatus.setStyleSheet("background:QColor(25,35,45);")
                self.ui.labelStatus.setText(txt+'(ONLINE)')
            else:
                self.ui.labelStatus.setStyleSheet("background-color: red")
                self.ui.labelStatus.setText(txt+'(OFFLINE)')
 




class KeyHelper(QObject):
    keyPressed = pyqtSignal(QtCore.Qt.Key)

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, source, event):
        if source is self.widget and event.type() == QEvent.KeyPress:
            self.keyPressed.emit(event.key())   
        return super().eventFilter(source, event)



class Clock(QObject):
    
    tick = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.running = True
     
    def run(self):
        while self.running:
            self.tick.emit(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            QtCore.QThread.msleep(1000)


    def stop(self):
        self.running = False



if __name__ == "__main__":
    main = Main()
