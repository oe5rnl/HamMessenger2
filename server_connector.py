#---------------------------------------------------------------------------------------------------------------
#  filename: server_connector.py
#  date: 2022-01-24
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3

from cgitb import text
import  time, os #, sys
import com
import hamgo_tcp
#import subprocess
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer

class Server(com.Com,QObject):
  
  def __init__(self,config): 
    super().__init__()
    print('INIT-server-connector')
    self.config = config

    
    # for ip change reconnect
    self.ip = self.config.serverIP
    self.port = self.config.serverPort
 
    self.config_data = None                          
    self.tcp = hamgo_tcp.Tcp()
 
    self.threadRx = QThread(parent=self)
    self.rx = RX()
    self.rx.moveToThread(self.threadRx)
    self.threadRx.started.connect(self.rx.run)  

    self.hb = HB(self.tcp,self.config)
    
  def start(self):
    self.threadRx.start()
 

  def stop(self):
    self.hb.timerHb.stop()
    self.rx.stop()
    self.threadRx.quit()
    self.tcp.stop()
    #print('server-connector:main terminated')
    
  def reconnect(self, force=False):
    #print(time.strftime("%a, %d %b %Y %H:%M:%S")+ ' start method-reconnect')
    if force:
      self.tcp.TCPclose()
      return self.TCPconnect(self.config.serverIP, self.config.serverPort)
    else:  
      if self.tcp.getConnected():
        return True      
      else:
        #print('do reconnect')
        return self.TCPconnect(self.config.serverIP, self.config.serverPort)

  def setConfig_data(self,config):
    self.config = config
 
  def TCPconnect(self, ip='localhost', port=9124):
    r = self.tcp.TCPconnect(self.config.serverIP, int(self.config.serverPort))
    print('server_connector:TCPconnect: '+str(r))
    return r



  def getTCPconnected(self):
    return self.tcp.getConnected()


class HB(QObject):

    def __init__(self,tcp,config):  
        super().__init__()
        self.tcp = tcp
        self.config = config

        self.timerHb=QTimer()
        self.timerHb.timeout.connect(self.heartbeat)

        QTimer.singleShot(5000, self.singleHb)

    def singleHb(self):
      self.heartbeat()
      self.timerHb.start(60000) # 1min


    def heartbeat(self):
        if self.tcp.getConnected():
            msg_text = self.config.name+'\t'+self.config.qth+'\t'+self.config.hamnetIP+'\t'+self.config.locator+'\t'+com.version
            msg = MSG(payloadType=0, payload=msg_text, contactType=1, source=self.config.call,) #+++
            b = msg.buildBarray()
            com.Com.queue_b2s.put(b) 

class RX(QObject):
    
    online_emit = pyqtSignal(object)
    close_emit = pyqtSignal(object)
    msg_emit = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.running = True
     
    def run(self):

        #print('server-connector: do_rx')
   
        while self.running:

          time.sleep(0.1)
          msgmax = 700
              
          #print('do_rx:queue_msg RECEIVED')
          try:
            msgbuf = com.Com.queue_msg.get(False)  
          except:
            pass
          else:
            if (len(msgbuf)<10):
              #print('len(msg) < 10 ->skipped !!!')
              continue

            lng = len(msgbuf)
            if (lng > msgmax):
              #print('len(msg) > '+str(msgmax)+' ->skipped !!!') 
              continue

            if ( (msgbuf[0]!=0xaa) and (msgbuf[1]!=0x00) and (msgbuf[2]!=0x00)  ): 
              #print('Bad msg rule: 6 STRONG ->skipped !!!')
              continue

            msg = MSG()
            msg.getMSGfromBuffer(msgbuf)
            #msg.printIPmsg('RX', mode='h')  
  
 
            # insert new GROUP
            if ((msg.PayloadType == MSG.c_PayloadGroupMessage)
                and (msg.ContactType == 1)
                and (msg.Contact=='GROUP')
                ): 
              pass

            # Heartbeat  & CQ
            elif ((msg.PayloadType == 0) #MSG.c_PayloadHaerdBeat)
                and (msg.ContactType == 1)
                and (msg.Contact=='CQ')
                ): 
              #print('\n\nHeartbeat  & CQ')
              payload = msg.Payload.split('\t')
              if msg.Payload[-5:] == 'CLOSE':
                    #print('msgCLOSE')
                    emsg = {}
                    emsg['PayloadTypeString'] = MSG.s_PayloadCQ
                    emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                    emsg['Source'] = msg.Source
                    emsg['Contact'] = msg.Contact
                    emsg['payload'] = 'CLOSE'
                    emsg['Path'] = msg.Path
                    self.close_emit.emit(emsg)                  

              elif len(payload)>5 : # CQ
                    #print('msg CQ')
                    emsg = {}
                    emsg['PayloadTypeString'] = MSG.s_PayloadCQ
                    emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                    emsg['Source'] = msg.Source
                    emsg['Contact'] = msg.Contact
                    emsg['payload'] = msg.Payload
                    emsg['Path'] = msg.Path
                    self.msg_emit.emit(emsg)    

              elif len(payload)==5:
                  print('server_connector:rx: (HB)')
                  emsg = {}
                  emsg['SeqCounter'] = msg.SeqCounter 
                  emsg['call'] = str(msg.Source)
                  emsg['name'] = str(payload[0])
                  emsg['info'] = str(payload[1])
                  emsg['ip'] = str(payload[2])
                  emsg['locator'] =  str(payload[3])
                  emsg['version'] =str(payload[4])
                  emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                  emsg['path'] = str(msg.Path)
                  #print('emsg='+str(emsg)+'\n')
                  emsg['Contact'] = 'HB' #msg.Contact
                  emsg['Path'] = msg.Path
                  self.online_emit.emit(emsg)
              else:
                  print('********************  PathType0 Error')
                  print('msg.Payload',msg.Payload)
                  print('msgSource', msg.Source)

            # Fehlerhaftes Paket !!!
            elif msg.Contact == "MSG":
                msg.printIPmsg('Error Packet: MSG') 
                emsg = {}
                # logging
          
            # BC Bradcast an alle
            elif ((msg.PayloadType == MSG.c_PayloadBroadcastMessage) # BC
                  and (msg.ContactType == 1)
                  and (msg.Contact=='ALL')
                ):    
                emsg = {}
                emsg['PayloadTypeString'] = msg.PayloadTypeString
                emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                emsg['Source'] = msg.Source
                emsg['Contact'] = msg.Contact
                emsg['payload'] = msg.Payload
                emsg['Path'] = msg.Path
                self.msg_emit.emit(emsg)

            # PC Personal Call
            elif ((msg.PayloadType == MSG.c_PayloadPrivateMessage) # PC
                  and (msg.ContactType == 1)
                  #and (msg.Contact=='ALL')  check calls'OE5RNL-L':
                 ):
                emsg = {}
                emsg['PayloadTypeString'] = msg.PayloadTypeString
                emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                emsg['Source'] = msg.Source
                emsg['Contact'] = msg.Contact
                emsg['payload'] = msg.Payload
                emsg['Path'] = msg.Path
                self.msg_emit.emit(emsg)
                       
            # Emergency Message
            elif ((msg.PayloadType == MSG.c_PayloadEmMessage) 
               and (msg.ContactType == 1) 
               and (msg.Contact=='EM') 
                  ): 
                  emsg = {}
                  emsg['PayloadTypeString'] = msg.s_PayloadEmMessage
                  emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                  emsg['Source'] = msg.Source
                  emsg['Contact'] = msg.Contact
                  emsg['payload'] = msg.Payload
                  emsg['Path'] = msg.Path
                  self.msg_emit.emit(emsg)
    
            # Group CALL
            elif ((msg.PayloadType == MSG.c_PayloadGroupMessage) 
               and (msg.ContactType == 1) 
               #and (msg.Contact=='ALL')  + Contact enthält die Gruppe
                  ):  
                emsg = {}
                emsg['PayloadTypeString'] = MSG.s_PayloadGroupMessage
                emsg['time'] = datetime.now() #str(time.strftime("%H:%M:%S"))
                emsg['Source'] = msg.Source
                emsg['Contact'] = msg.Contact
                emsg['payload'] = msg.Payload
                emsg['Path'] = msg.Path
                self.msg_emit.emit(emsg)

            # Unknowmn Message
            else:
              msg.printIPmsg('Unknowmn Message')
    
            del msg
            #del emsg

        print("rx loop ende")

    def stop(self):
        #print("****RX:do_stop")
        self.running = False

    def errorMsg(self, state, source, contact, payload):
        emsg = {}
        if state == 'ok':
          emsg['PayloadTypeString'] = MSG.s_PayloadErrOkMessage
        else:
          emsg['PayloadTypeString'] = MSG.s_PayloadErrErMessage
        emsg['time'] = datetime.now()
        emsg['Source'] = source
        emsg['Contact'] = contact
        emsg['payload'] = payload
        emsg['Path'] = ""
        self.msg_emit.emit(emsg)


class Send(QObject):

  def __init__(self,config):
      super().__init__()
      self.bc_i = 1
      self.gc_i = 1
      self.cq_i = 1
      self.config = config

  def HB(self):
      print('Send:HB')
      msg_text = self.config.name+'\t'+self.config.qth+'\t'+self.config.hamnetIP+'\t'+self.config.locator+'\t'+com.version
      msg = MSG(payloadType=0, payload=msg_text, contactType=1, source=self.config.call,) 
      b = msg.buildBarray()
      com.Com.queue_b2s.put(b) 

  def CLOSE(self):
      msg_text = self.config.name+'\t'+self.config.qth+'\t'+self.config.hamnetIP+'\t'+self.config.locator+'\tCLOSE' 
      msg = MSG(payloadType=0, payload=msg_text, contactType=1, source=self.config.call,) 
      b = msg.buildBarray()
      com.Com.queue_b2s.put(b) 

  def BC(self,text):
      msg_text = '('+str(self.bc_i)+') '+text
      msg = MSG(payloadType=MSG.c_PayloadBroadcastMessage, payload=msg_text, contactType=1, contact='ALL', source=self.config.call)   
      b = msg.buildBarray()   
      com.Com.queue_b2s.put(b)         
      self.bc_i +=1

  def CQ(self,text): ##+ self.config.hamnetIP+'\t' \
      msg_text =  self.config.name+'\t'+ self.config.qth+'\t' + self.config.hamnetIP+'\t'+self.config.locator+'\t'+ com.version+'\t(' + str(self.cq_i)+') '+text 
      msg = MSG(payloadType=0, payload=msg_text, contactType=1, contact='CQ', source=self.config.call)   
      b = msg.buildBarray()   
      msg.printIPmsg('+++++')
      com.Com.queue_b2s.put(b)         
      self.cq_i += 1

  def GC(self,group,text):
      msg_text = '('+str(self.gc_i)+') '+text 
      msg = MSG(payloadType=MSG.c_PayloadGroupMessage, payload=msg_text, contactType=1, contact=group, source=self.config.call)   
      b = msg.buildBarray()   
      com.Com.queue_b2s.put(b)         
      self.gc_i += 1

  def PC(self,call,text):
      msg = MSG(payloadType=MSG.c_PayloadPrivateMessage, payload=text, contactType=1, contact="'"+call, source=self.config.call)   
      b = msg.buildBarray()   
      com.Com.queue_b2s.put(b)         
      self.gc_i += 1

  def EC(self,text):
      msg = MSG(payloadType=MSG.c_PayloadEmMessage, payload=text, contactType=1, contact='EM', source=self.config.call)   
      b = msg.buildBarray()   
      com.Com.queue_b2s.put(b)         
      self.gc_i += 1


class MSG:

  # Payload types
  c_PayloadHaerdBeat         = 0 # 0 
  c_PayloadCQ                = 0 # 0
  c_Payload1                 = 1 # 1
  c_PayloadPrivateMessage    = 2 # 2
  c_Payload3                 = 3 # 3
  c_PayloadGroupMessage      = 4 # 4
  c_Payload5                 = 5 # 5
  c_PayloadBroadcastMessage  = 6 # 6
  c_PayloadEmMessage         = 7 # 7

  s_PayloadHaerdBeat         = 'SE'
  s_PayloadCQ                = 'CQ'
  s_Payload_1                = 'P1'
  s_PayloadPrivateMessage    = 'PC'
  s_Payload_3                = 'P3' 
  s_PayloadGroupMessage      = 'GC'
  s_Payload_5                = 'P5' 
  s_PayloadBroadcastMessage  = 'BC'  
  s_PayloadEmMessage         = 'EM' 
  s_PayloadErrErMessage      = 'ER'
  s_PayloadErrOkMessage      = 'OK'
  

  def __init__(self, version=1, ttl=0xfe, flags=0x00,source='', contactType=0x01, contact='CQ', path='', payloadType=0x00, payload='' ):

    # Reihenfole entspricht der im Datenpaket
    self.Version = version          # 2 Byte  big-endian
    self.SeqCounter = os.urandom(8) # 8 Byte  
    self.TTL = ttl                  # 1 Byte
    self.Flags=flags                # 1 Byte
    self.SourceLength=0             # 2 Byte  big-endian
    self.Source = source            # 0-n Byte
    self.ContactType = contactType  # 1 Byte
    self.ContactLength=0            # 2 Byte  big-endian
    self.Contact = contact          # 0-n Byte
    self.PathLength=0               # 2 Byte  big-endian
    self.Path = path                # 0-n Byte
    self.PayloadType = payloadType  # 1 Byte
    self.PayloadLength=0            # 4 Byte  little-endian
    self.Payload = payload          # 0-n Byte

    self.PayloadTypeString=''
    self.PayloadText = ''

    self.SourceLength =  len(self.Source)
    self.ContactLength =  len(self.Contact)  
    self.PathLength =  len(self.Path)     
    self.PayloadLength =  len(self.Payload)

  def buildBarray(self): 
    #print('buildBarray: start... ', end='')

    # Start Frame
    b = 0xaa.to_bytes(1, byteorder='little')
    
    # Version
    b +=  self.Version.to_bytes(2, byteorder='little')
    # Sequence Counter
    b += self.SeqCounter
    # TTL
    b += self.TTL.to_bytes(1, byteorder='little')
    # Flags
    b += self.Flags.to_bytes(1, byteorder='little')
    
    #Source = call
    t = self.Source.encode(encoding='UTF-8')
    l = len(t)
    # Source length
    b += l.to_bytes(2, byteorder='big')
    # Source
    if l > 0:
      b += t
  
    # Contact Type
    b += self.ContactType.to_bytes(1, byteorder='little')
    
    # Contact 
    t = self.Contact.encode(encoding='UTF-8')
    l = len(t)    
    # Contact length
    b += l.to_bytes(2, byteorder='big')
    if l > 0:
      # contact
      b += t

    # Path
    t = self.Path.encode(encoding='UTF-8')
    l = len(t)
    # Path length
    b += l.to_bytes(2, byteorder='little')
    if l > 0:
      # path
      b += t

    # Payloadtype
    b += self.PayloadType.to_bytes(1, byteorder='little')

    if self.PayloadType == b'\x02':
      self.PayloadLength = 7
      self.Payload = b'\x00\x04\x00\x00\x00\x00\x00'

    # payload 
    t = self.Payload.encode(encoding='UTF-8')
    l = len(t)
    # payload length
    b += l.to_bytes(4, byteorder='little')
    # payload
    if l > 0:
      # payload value
      b += t
    
    # end frame
    b += 0xab.to_bytes(1, byteorder='little')
    
    #print('buildBarray: ende')
    return b

  def getMSGfromBuffer(self, msgbuf):
    #print('getMSGfromBuffer:lng='+str(lng))
    ibp = 1

    try:

      #print('getMSGfromBuffer:'+str(msgbuf))
      if ( (msgbuf[1]==0x00) and (msgbuf[2]==0x00) ):
        #print('getMSGfromBuffer:problem')
        return 'x'

      # Version
      self.Version = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='little')
      ibp = ibp + 2

      if self.Version == 0:
        return

      self.SeqCounter = int.from_bytes(msgbuf[ibp:ibp+8],byteorder='little')
      ibp = ibp + 8

      self.TTL = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1

      self.Flags = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1

      self.SourceLength = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='big')
      ibp = ibp + 2

      self.Source = msgbuf[ibp:ibp+self.SourceLength].decode('utf-8')
      ibp = ibp + self.SourceLength

      self.ContactType = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1

      self.ContactLength = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='big')
      ibp = ibp + 2

      self.Contact = msgbuf[ibp:ibp+self.ContactLength].decode('utf-8')
      ibp = ibp + self.ContactLength
              
      self.PathLength = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='little')
      ibp = ibp + 2

      self.Path = msgbuf[ibp:ibp+self.PathLength].decode('utf-8')
      ibp = ibp + self.PathLength

      self.PayloadType = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1    

      self.PayloadLength = int.from_bytes(msgbuf[ibp:ibp+4],byteorder='little')
      ibp = ibp + 4

      self.Payload = msgbuf[ibp:ibp+self.PayloadLength].decode("utf-8")

      self.PayloadTypeString = "CQ"

      if (self.PayloadType == 0): self.PayloadTypeString = MSG.s_PayloadHaerdBeat 
      elif (self.PayloadType == 2): self.PayloadTypeString = MSG.s_PayloadPrivateMessage 
      elif (self.PayloadType == 4): self.PayloadTypeString = MSG.s_PayloadGroupMessage 
      elif (self.PayloadType == 6): self.PayloadTypeString = MSG.s_PayloadBroadcastMessage 
      elif (self.PayloadType == 7): self.PayloadTypeString = MSG.s_PayloadEmMessage 
      else:
          self.PayloadTypeString ="ER1"

    except ValueError:
      self.PayloadTypeString = "ER"
      self.Source = self.Source
      self.Contact = "MSG"
      self.PayloadText = "Protocol-Error in the last received message"

    return self


  def printIPmsg(self, title='', mode='m'):
      print()
      if mode == 'm':   
          print(title)
          print('Version='+str(self.Version))
          print('SeqCounter='+str(self.SeqCounter))
          print('TTL='+str(self.TTL))
          print('Flags='+str(self.Flags))
          print('SourceLength='+str(self.SourceLength))
          print('Source='+str(self.Source))
          print('ContactType='+str(self.ContactType))
          print('ContactLength='+str(self.ContactLength))
          print('Contact='+str(self.Contact))
          print('PathLength='+str(self.PathLength))
          print('Path='+str(self.Path))
          print('PayloadType='+str(self.PayloadType))
          print('PayloadLength='+str(self.PayloadLength))
          print('Payload='+str(self.Payload))      
          print('PayloadTypeString='+str(self.PayloadTypeString))
      else:    
          print(str(self))
          print(title+': '
            + ' Version='+str(self.Version)
            + ' SeqCounter='+str(self.SeqCounter)
            + ' TTL='+str(self.TTL)
            + ' Flags='+str(self.Flags)
            + ' SourceLength='+str(self.SourceLength)
            + ' Source='+str(self.Source)
            + ' ContactType='+str(self.ContactType)
            + ' ContactLength='+str(self.ContactLength)
            + ' Contact='+str(self.Contact)
            + ' PathLength='+str(self.PathLength)
            + ' Path='+str(self.Path)
            + ' PayloadType='+str(self.PayloadType)
            + ' PayloadLength='+str(self.PayloadLength)
            + ' Payload=|'+str(self.Payload)+'|'
            + ' PayloadTypeString='+str(self.PayloadTypeString)
          )        

 
