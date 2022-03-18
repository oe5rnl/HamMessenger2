#---------------------------------------------------------------------------------------------------------------
#  filename: qt_group.py
#  date: 2022-01-24
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3

import os

from PyQt5.QtCore import QObject, QRegExp
from PyQt5.QtWidgets import (QMessageBox)
import configparser
from PyQt5 import QtGui, uic
from PyQt5.QtGui import QRegExpValidator
import get_OS

class GroupDialog(QObject):

    def __init__(self,ui,config):
        super().__init__()
        self.ui = ui
        self.config = config
        
        self.clearCbx()
        self.ui.comboBoxGroup.currentIndexChanged.connect(self.on_groupChange)
        self.dlg_ui = uic.loadUi(get_OS.getAPPPath()+"newgroup.ui")
        self.dlg_ui.setWindowIcon(QtGui.QIcon(get_OS.getAPPPath()+"res/worldwide.png")) 
        self.dlg_ui.buttonBox.accepted.connect(self.on_newGroup)
        self.dlg_ui.setModal(True)
        self.ui.pushButtonDeleteGroup.clicked.connect(self.on_delete)

        reg_ex = QRegExp("[a-z-A-Z_1-9]+")
        self.dlg_ui.lineEditGroupID.setValidator(QRegExpValidator(reg_ex, self.dlg_ui.lineEditGroupID))

        reg_ex = QRegExp("[a-z-A-Z_1-9 ]+")
        self.dlg_ui.lineEditGroupDesc.setValidator(QRegExpValidator(reg_ex, self.dlg_ui.lineEditGroupDesc))
      
        self.groupsFile = get_OS.getUserDataPath()+'groups.ini'    
        self.groups = configparser.ConfigParser()
        self.groups.optionxform = str # makes configparser case sensitive
        self.read_groups()
      
    def getGroup(self):
        key = self.ui.comboBoxGroup.currentText().split(' : ')  
        return key[0]

    def clearCbx(self):
        self.ui.comboBoxGroup.clear()
        self.ui.comboBoxGroup.addItems(['please select group','insert new group...']) 

    def isValidGroup(self, group):
        if group not in ['please select group','insert new group...']:
            return True
        return False


    def on_delete(self):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Delete ?")
        msgBox.setWindowTitle("Delete Group")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            key = self.ui.comboBoxGroup.currentText().split(' : ')
            self.groups.remove_option('GROUPS', key[0])  
            self.ui.comboBoxGroup.removeItem(self.ui.comboBoxGroup.findText(self.ui.comboBoxGroup.currentText()))
            self.write_groups()

    def write_groups(self):
        with open(self.groupsFile, 'w') as configfile:
            self.groups.write(configfile)
 
    def read_groups(self):
        self.groups.read(self.groupsFile)
        if not self.groups.has_section('GROUPS'):
            self.groups.add_section('GROUPS')
   
        self.clearCbx()
        for e in dict(self.groups.items('GROUPS')):
            #print(e + ' '+self.groups.get('GROUPS',e))
            self.ui.comboBoxGroup.addItem(e + ' : '+self.groups.get('GROUPS',e))
        
    def on_groupChange(self):

        if (self.ui.comboBoxGroup.currentText() == 'insert new group...') or (self.ui.comboBoxGroup.currentText() == 'please select group'):
            self.ui.pushButtonDeleteGroup.setEnabled(False)
        else:
            self.ui.pushButtonDeleteGroup.setEnabled(True)

        if self.ui.comboBoxGroup.currentText() == 'insert new group...':

            self.dlg_ui.show()

    def on_newGroup(self):

        if  ( (len(self.dlg_ui.lineEditGroupID.text())>0) and (len(self.dlg_ui.lineEditGroupDesc.text())>0) ):

            self.groups['GROUPS'][self.dlg_ui.lineEditGroupID.text().strip().upper()] = self.dlg_ui.lineEditGroupDesc.text().strip()
            self.write_groups()
            self.read_groups()
  
            txt = self.dlg_ui.lineEditGroupID.text()+' : '+self.dlg_ui.lineEditGroupDesc.text()
            index = self.ui.comboBoxGroup.findText(txt)
            self.ui.comboBoxGroup.setCurrentIndex(index)

            self.dlg_ui.lineEditGroupID.setText('')
            self.dlg_ui.lineEditGroupDesc.setText('')


