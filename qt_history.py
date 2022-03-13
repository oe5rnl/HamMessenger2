#---------------------------------------------------------------------------------------------------------------
#  filename: qt_history.py
#  date: 2022-01-24
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3


from PyQt5.QtWidgets import (QTableWidgetItem)
from PyQt5.uic import *
from PyQt5.QtCore import QObject
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui



class History(QObject):

    def __init__(self,ui,guimode,config):
        super().__init__()
        self.ui = ui
        self.guimode = guimode
        self.config = config

        self.row = -1

        self.ui.tableWidgetHistory.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidgetHistory.setColumnCount(5)
        self.ui.tableWidgetHistory.horizontalHeader().setVisible(True)
        self.ui.tableWidgetHistory.setHorizontalHeaderLabels(["Typ", "Time", "Src", "Dst", "Text"])
        #header =  self.ui.tableWidgetHistory.horizontalHeader()       
   

   
        self.ui.tableWidgetHistory.setColumnWidth(0, 50)
        self.ui.tableWidgetHistory.setColumnWidth(1, 70)
        self.ui.tableWidgetHistory.setColumnWidth(2, 80)
        self.ui.tableWidgetHistory.setColumnWidth(3, 100)
        self.ui.tableWidgetHistory.setColumnWidth(4, 500)

        #header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)


    def append(self,emsg):
        
        # receive only used groups
        if emsg['PayloadTypeString'] == "GC":  
        
            # Gruppen aus der Combobox --> PFUI !!!
            l = [self.ui.comboBoxGroup.itemText(i) for i in range(self.ui.comboBoxGroup.count())] 
            l.pop(0)   
            l.pop(0)  
            l = [l[i].split(':')[0].strip() for i in range(len(l))]   
            if emsg['Contact'] not in l:
                 return

        # receive only messages for me and from me
        elif emsg['PayloadTypeString'] == "PC":      
            if emsg['Source'] == self.config.call:
                pass
            else:
                if emsg['Contact'] != "'"+self.config.call:
                    return

        self.row += 1
        self.ui.tableWidgetHistory.setRowCount(self.row+1)

        color = QtGui.QColor(5,5,5)  


        if self.guimode.getMode() == 'light':

            if emsg['PayloadTypeString'].strip() == "BC":
                fcolor = QtGui.QColor(0,0,0)   
                bcolor = QtGui.QColor(255,255,255)   
            elif emsg['PayloadTypeString'] == "CQ":  
                fcolor = QtGui.QColor(0,0,0)   
                bcolor = QtGui.QColor(255,255,0)                     
            elif emsg['PayloadTypeString'] == "GC":
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(42,128,0)  
            elif emsg['PayloadTypeString'] == "PC":
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(42,128,0)           
            elif emsg['PayloadTypeString'] == "EM":
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(255,0,0)  

            else:
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(25,35,45)

        else:
            if emsg['PayloadTypeString'] == "BC":    
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(25,35,45)   
            elif emsg['PayloadTypeString'] == "CQ":  
                fcolor = QtGui.QColor(0,0,0)   
                bcolor = QtGui.QColor(255,255,0)     
            elif emsg['PayloadTypeString'] == "GC":
                fcolor = QtGui.QColor(0,0,0)   
                bcolor = QtGui.QColor(42,128,0)  
            elif emsg['PayloadTypeString'] == "PC":
                fcolor = QtGui.QColor(0,0,0)   
                bcolor = QtGui.QColor(42,128,0)
            elif emsg['PayloadTypeString'] == "EM":
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(255,0,0) 
            elif emsg['PayloadTypeString'] == "ER":
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(255,0,0)   
            elif emsg['PayloadTypeString'] == "OK":
                fcolor = QtGui.QColor(0,0,0)   
                bcolor = QtGui.QColor(144,238,144)                                 
            else:
                fcolor = QtGui.QColor(255,255,255)   
                bcolor = QtGui.QColor(25,35,45)
  
        self.ui.tableWidgetHistory.setItem(self.row,0, QTableWidgetItem(emsg['PayloadTypeString']))
        self.ui.tableWidgetHistory.setItem(self.row,1, QTableWidgetItem(emsg['time'].strftime("%H:%M:%S"))) 
        self.ui.tableWidgetHistory.setItem(self.row,2, QTableWidgetItem(emsg['Source']))
        self.ui.tableWidgetHistory.setItem(self.row,3, QTableWidgetItem(emsg['Contact']))
        self.ui.tableWidgetHistory.setItem(self.row,4, QTableWidgetItem(emsg['payload']))
        
        for j in range(self.ui.tableWidgetHistory.columnCount()):
            self.ui.tableWidgetHistory.item(self.row, j).setBackground(bcolor)
        for j in range(self.ui.tableWidgetHistory.columnCount()):
            self.ui.tableWidgetHistory.item(self.row, j).setForeground(fcolor)

        self.ui.tableWidgetHistory.scrollToBottom()   
        self.ui.tableWidgetHistory.resizeRowsToContents()

        # Soundausgabe fehlt

