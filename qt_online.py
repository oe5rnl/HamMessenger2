#---------------------------------------------------------------------------------------------------------------
#  filename: qt_online.py
#  date: 2022-01-24
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3



from PyQt5.QtWidgets import (QTableView)
from PyQt5 import QtWidgets
from PyQt5 import (QtCore, Qt)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush,QColor

import datetime
from datetime import datetime, timedelta

from operator import itemgetter

class OnlineTableView(QTableView): 

    #calls_changed = pyqtSignal(object)

    def __init__(self,ui,config):
        super().__init__()
        self.ui = ui
        self.config = config

        self.ui.tableViewOnline.verticalHeader().hide()

        self.model = TableModel()    
        self.ui.tableViewOnline.setModel(self.model)
        header =  self.ui.tableViewOnline.horizontalHeader()       
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)

        self.ui.tableViewOnline.setColumnHidden(9,True)
        self.ui.tableViewOnline.setColumnHidden(10,True)
        
        self.ui.tableViewOnline.verticalHeader().setDefaultSectionSize(20)

        self.ui.tableViewOnline.setColumnWidth(0, 100)   # status
        self.ui.tableViewOnline.setColumnWidth(1, 100)   # call
        self.ui.tableViewOnline.setColumnWidth(2, 100)   # name
        self.ui.tableViewOnline.setColumnWidth(3, 200)   # Info    
        self.ui.tableViewOnline.setColumnWidth(4, 100)   # LOC
        self.ui.tableViewOnline.setColumnWidth(5, 80)    # LH
        self.ui.tableViewOnline.setColumnWidth(6, 100)   # IP
        self.ui.tableViewOnline.setColumnWidth(7, 80)    # Version
        self.ui.tableViewOnline.setColumnWidth(8, 200)   # Path
          
    def getValue(self,r,c):
        if (r<=len(self.model.mdata)) and (c<=len(self.model.mdata[0])):   # WORKAROUND !!!
            return self.model.mdata[r][c]
        return ""

    def getCall(self,row):
        return self.model.mdata[row][1]

    def erase(self):
        self.model.erase()

    def append(self,emsg):

        self.model.addData(emsg)

        self.ui.tableViewOnline.resizeColumnsToContents()
        self.ui.tableViewOnline.resizeRowToContents(7)
   
        self.model.layoutChanged.emit()
        self.ui.tableViewOnline.scrollToBottom()

    def closeCall(self,emsg):
        self.model.closeCall(emsg['Source'])
        self.model.layoutChanged.emit()

    def get_grid(self,i):
        return self.getValue(i.row(),7).strip()

    def getCalls(self):
        return self.model.getCalls()


class TableModel(QtCore.QAbstractTableModel):

    calls_changed = pyqtSignal(object)

    def __init__(self):
        super(TableModel, self).__init__()
        self.mdata = [["","","","","","","","","",datetime,""]]
        self.headers = ["status", "Call", "Name", "Info", "LOC", "LH", "IP", "Version", "Path", "time", "sort"]

        self.online = []
        self.offline = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            #print("index.row:"+str(index.row())+" index.col:"+str(index.column()),"role:"+str(role))
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            #print('A='+str(self.mdata[index.row()][index.column()]))
            #if index.column()==9:
            #    print('++++'+ str(type(self.mdata[index.row()][index.column()])))
            #    return '*' #self.mdata[index.row()][index.column()]).strftime("%H:%M:%S")
            #else:
                return str(self.mdata[index.row()][index.column()])

        elif role == Qt.BackgroundRole:
            #if index.row() % 2 == 0:
                #return QBrush(Qt.green)
                #print(self.mdata[index.row()][index.column()])
                if self.mdata[index.row()][0] == 'online':
                    return QBrush(QColor(144,238,144))
                elif self.mdata[index.row()][0] == 'offline':
                    return QBrush(QColor(255,160,122))

        elif role == Qt.ForegroundRole:
            #if index.row() % 2 == 0:
                #return QBrush(Qt.green)    
                if self.mdata[index.row()][0] == 'online':
                    return QBrush(QColor(0,0,0))
                elif self.mdata[index.row()][0] == 'offline':
                    return QBrush(QColor(0,0,0))

    def getCalls(self):
        #print('model:call:emit')
        calls=[]
        for e in self.mdata:
            if e[0] == 'online':
                calls.append(e[1])
        return(calls)


    # online list management
    def isInList(self,call,status):
        found = False
        row=''
        col=''
        for row, col in enumerate(self.mdata):
            if col[1] == call and col[0] == status:
                found=True
                break
        return found, row, col

    def append(self,newRow,status):
        p = 0
        newRow[0] = status
        if status == 'online': 
            newRow[10] = 'A' 
        else:  newRow[10] = 'B'
        self.mdata.append(newRow)
        self.calls_changed.emit(self.getCalls())
        
    def update(self, data):
        dt =  datetime.now()
        for e in self.mdata:
            if e[1] == data[1]:
                e[2] = data[2]
                e[3] = data[3]
                e[4] = data[4]
                e[5] = dt.strftime("%H:%M:%S")     
                e[9] = dt 
                e[6] = data[6]


    def emsg2data(self,emsg):
        return ['',emsg['call'],emsg['name'],emsg['info'],emsg['locator'],emsg['time'].strftime("%H:%M:%S") ,emsg['ip'],emsg['version'],emsg['path'],emsg['time'],'']
                

    def addData(self,emsg):

        # delete empty line
        if self.mdata[0][0] == '':
            del self.mdata[0]

        data = self.emsg2data(emsg)
      
        pon,  rowOn, colsOn = self.isInList(emsg['call'],'online')
        poff, rowOff, colsOff  = self.isInList(emsg['call'],'offline')  

        # wenn offline, dann wieder auf online
        if poff: 
            self.mdata.pop(rowOff)
            self.append(data,'online')

        # Update wenn vorhanden, sonst insert     
        elif pon: 
            self.update(data)

        # neu eintragen wenn noch nicht vorhanden
        elif not pon and not poff:
            self.append(data,'online')

        else:
            print('ERROR: pon poff')

        # timeout()
        for row, cols in enumerate(self.mdata):   
            if cols[0] == 'online':
                if cols[9] < datetime.now()-timedelta(seconds=120):
                    self.mdata.pop(row)
                    self.append(cols,'offline')  
                    self.calls_changed.emit(self.getCalls())
        
        self.mdata = sorted(self.mdata, key=itemgetter(10,1))


    def closeCall(self,call):      
        #print('model.closecall')  
        p, row, cols = self.isInList(call,'online')
        cols[0]  = 'offline'
        cols[10] = 'B'
        
        self.mdata = sorted(self.mdata, key=itemgetter(10,1))
        self.calls_changed.emit(self.getCalls())


    def rowCount(self, index=None):
        # The length of the outer list.
        return len(self.mdata)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self.mdata[0])

    # def headerData(self, col, orientation, role):
    #     if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #         return QVariant(self.headerdata[col])
    #     return QVariant()

    def headerData(self, section, orientation, role):
        if role !=Qt.DisplayRole or orientation != Qt.Horizontal:
            return QtCore.QVariant()
        # What's the header for the given column?
        return self.headers[section]
