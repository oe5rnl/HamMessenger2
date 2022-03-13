#---------------------------------------------------------------------------------------------------------------
#  filename: qt_msglog.py
#  date: 2022-01-24
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3



import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem)
from PyQt5.QtCore import QObject

from pysondb import db

import get_OS

# https://dev.to/fredysomy/pysondb-a-json-based-lightweight-database-for-python-ija

class TableWidgetLog(QObject):

    def __init__(self,ui):
        super().__init__()
        self.ui = ui

        self.logdb=db.getDb(get_OS.getUserDataPath()+"HamMessenger2_log.json")

        self.ui.dateTimeEdit.setDateTime(datetime.datetime.now())
        self.ui.dateTimeEdit.dateChanged.connect(self.do_date)

        self.ui.tableWidget_Log.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_Log.setColumnCount(6)   
        self.ui.tableWidget_Log.horizontalHeader().setVisible(True)

        self.ui.tableWidget_Log.setHorizontalHeaderLabels(['Time', 'Type', 'Src', 'Dst', 'Text','Path'])

        self.ui.tableWidget_Log.setColumnWidth(0, 150)
        self.ui.tableWidget_Log.setColumnWidth(1, 50)
        self.ui.tableWidget_Log.setColumnWidth(2, 100)
        self.ui.tableWidget_Log.setColumnWidth(3, 50)
        self.ui.tableWidget_Log.setColumnWidth(4, 300)
        self.ui.tableWidget_Log.setColumnWidth(5, 300)

        self.row = -1

        self.fill(self.getDayList(self.ui.dateTimeEdit.date().toPyDate()))


    def getDayList(self,day):
        t = self.ui.dateTimeEdit.date().toPyDate()
        return self.logdb.getByQuery({"date": str(t.year)+f"{t.month:02d}"+f"{t.day:02d}"}) 


    def do_date(self):
        self.fill(self.getDayList(self.ui.dateTimeEdit.date().toPyDate()))
        

    def fill(self,l):
        self.ui.tableWidget_Log.setRowCount(0)
        self.row = -1
        for e in l:
            self.appendToTable(e)



    def appendToTable(self,e):
        self.row += 1
        self.ui.tableWidget_Log.setRowCount(self.row+1)
    
        self.ui.tableWidget_Log.setItem(self.row,0, QTableWidgetItem(e['date']))
        self.ui.tableWidget_Log.setItem(self.row,0, QTableWidgetItem(str(e['time'])))
        self.ui.tableWidget_Log.setItem(self.row,1, QTableWidgetItem(e['PayloadTypeString']))
        self.ui.tableWidget_Log.setItem(self.row,2, QTableWidgetItem(e['Source']))
        self.ui.tableWidget_Log.setItem(self.row,3, QTableWidgetItem(e['Contact']))
        self.ui.tableWidget_Log.setItem(self.row,4, QTableWidgetItem(e['payload']))
        if 'Path' in e:
            self.ui.tableWidget_Log.setItem(self.row,5, QTableWidgetItem(e['Path']))
        else:
            self.ui.tableWidget_Log.setItem(self.row,5, QTableWidgetItem(''))

        self.ui.tableWidget_Log.resizeRowsToContents()



    def append2Log(self,emsg):
        dt = emsg['time']
        emsg['date'] = str(dt.year)+f"{dt.month:02d}"+f"{dt.day:02d}"    
        emsg['time'] = "{0}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format(dt.year,dt.month,dt.day, dt.hour,dt.minute,dt.second)
        self.logdb.add(emsg)
        self.fill(self.getDayList(self.ui.dateTimeEdit.date().toPyDate()))


