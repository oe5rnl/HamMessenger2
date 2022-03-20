#---------------------------------------------------------------------------------------------------------------
#  filename: qt_config.py
#  date: 2022-01-24
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3

from PyQt5.QtCore import QObject, QSettings, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox
import get_OS


class Config(QObject):

    guimode_emit = pyqtSignal(object)
    testTone_emit = pyqtSignal(object)
    save_emit = pyqtSignal()


    def __init__(self,ui):
        super().__init__()

        self.ui = ui

        self.configfile = get_OS.getUserDataPath()+'application.ini'
        self.settings = QSettings(self.configfile, QSettings.IniFormat)

        self.ui.comboBoxGuiStyle.currentIndexChanged.connect(self.on_guiModeChange)
        self.ui.pushButtonSave.clicked.connect(self.do_save)
        self.ui.pushButtonTone.clicked.connect(self.do_tone)

        self.read_config()
        self.setGuiValues()


    def do_tone(self):
        self.testTone_emit.emit(self.guimode)

    def read_config(self):

        self.call        = self.settings.value('HAMGO-CLIENT/call','')
        self.name        = self.settings.value('HAMGO-CLIENT/name','1')
        self.qth         = self.settings.value('HAMGO-CLIENT/qth','2')
        self.locator     = self.settings.value('HAMGO-CLIENT/locator','3')
        self.serverIP    = self.settings.value('HAMGO-CLIENT/serverIP','44.143.0.1')   # 44.143.9.72
        self.hamnetIP    = self.settings.value('HAMGO-CLIENT/hamnetIP','44.')
        self.serverPort  = self.settings.value('HAMGO-CLIENT/port','9124')
        self.log         = self.settings.value('HAMGO-CLIENT/log','12')
        self.audio       = self.settings.value('HAMGO-CLIENT/audio','13')
        self.guimode     = self.settings.value('HAMGO-CLIENT/guimode','dark')
        self.alert       = self.settings.value('HAMGO-CLIENT/alert', True, type=bool)
        self.sendbyenter = self.settings.value('HAMGO-CLIENT/sendbyenter', True, type=bool)


        self.mainWSize  = self.settings.value('GUI/mainWSize','1300,800')       

        if self.settings.value('gui/splitterH') is not None:
            self.ui.splitterH.restoreState(self.settings.value('GUI/splitterH'))

        if self.settings.value('gui/splitterV') is not None:
            self.ui.splitterV.restoreState(self.settings.value('GUI/splitterV'))
          
     
    def write_config(self):
        self.settings.setValue('HAMGO-CLIENT/call', self.call)
        self.settings.setValue('HAMGO-CLIENT/name', self.name)
        self.settings.setValue('HAMGO-CLIENT/qth', self.qth)
        self.settings.setValue('HAMGO-CLIENT/locator', self.locator)
        self.settings.setValue('HAMGO-CLIENT/serverIP',self.serverIP)
        self.settings.setValue('HAMGO-CLIENT/hamnetIP',self.hamnetIP)
        self.settings.setValue('HAMGO-CLIENT/guimode',self.guimode)
        self.settings.setValue('HAMGO-CLIENT/alert',self.alert)
        self.settings.setValue('HAMGO-CLIENT/sendbyenter',self.sendbyenter)

        self.settings.setValue('GUI/mainWSize',self.mainWSize)

        self.settings.setValue('GUI/splitterH', self.ui.splitterH.saveState())  
        self.settings.setValue('GUI/splitterV', self.ui.splitterV.saveState())  


        self.settings.sync()

    
    def addServer(self,server):
        self.server = server


    def on_guiModeChange(self):
        self.guimode = self.ui.comboBoxGuiStyle.currentText()
        self.guimode_emit.emit(self.guimode)


    def do_save(self):

        if len(self.ui.lineEditCall.text().strip())==0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("please set a valid call!")
            msgBox.setWindowTitle("HamMessenger Config")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return

        self.call = self.ui.lineEditCall.text().upper()  
        self.name = self.ui.lineEditName.text()      
        self.qth = self.ui.lineEditQTH.text()      
        self.locator = self.ui.lineEditLocator.text().upper()   
        self.serverIP = self.ui.lineEditServerIP.text()
        self.hamnetIP = self.ui.lineEditHamnetIP.text()
        self.guimode = self.ui.comboBoxGuiStyle.currentText()
        self.alert = self.ui.checkBoxAlertTone.isChecked()
        self.sendbyenter = self.ui.checkBoxSendByEnter.isChecked()
        self.write_config()

        #self.label_2.setStyleSheet("background-color: yellow; border: 1px solid black;")
        self.ui.labelSaveState.setStyleSheet("color: #FF0000; border: 1px solid black; font-size=22")
        print('1')
        self.save_emit.emit()
        #print('2')

        self.ui.labelSaveState.setText('saved')
        QTimer.singleShot(1000, self.save_label)

    def save_label(self):
        self.ui.labelSaveState.setText('')     

    def setGuiValues(self):
        self.ui.lineEditCall.setText(self.call)     
        self.ui.lineEditName.setText(self.name)      
        self.ui.lineEditQTH.setText(self.qth)      
        self.ui.lineEditLocator.setText(self.locator)       

        self.ui.lineEditServerIP.setText(self.serverIP)  #
        self.ui.lineEditHamnetIP.setText(self.hamnetIP)  

        self.ui.comboBoxGuiStyle.setCurrentText(self.guimode)

        self.ui.checkBoxAlertTone.setChecked(self.alert)
        self.ui.checkBoxSendByEnter.setChecked(self.sendbyenter)
        

        self.ui.labelAppPath.setText(get_OS.getAPPPath())
        self.ui.labelAppDataPath.setText(get_OS.getUserDataPath())
        self.ui.labelLogPath.setText(get_OS.getUserDataPath())


