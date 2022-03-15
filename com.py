#---------------------------------------------------------------------------------------------------------------
#  filename: server_connector.py
#  date: 2022-02-18
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux, Mac und Windows
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3

import time, queue 

version = 'U.0.5.6a'
date = '2020-03-15'


#--------------------------------------------------
class Com():

  queue_msg = queue.Queue() # Data from msg_dispatcher to serverconnetor
  queue_s2h = queue.Queue() # Data from msg_dispatcher to history
  queue_s2o = queue.Queue() # Server sendet zu online 
  queue_b2s = queue.Queue() # Broadcast to server


def isascii(c):
  return ( (c >= 0x20) and (c<=0x7f) )

def p(c):
  if isascii(c):
    return(chr(c))
  else:
    return(hex(c))

def pb(buf, h=''):
  print(h+'len='+str(len(buf)))
  for i in buf:
    x = str(hex(i))
    x = x.replace("0x", "")
    if len(x) == 1:
      x='0'+x
    else:
      x= ''+x
    print(x+' ', end='')
print('')

def escape(inbuf):

  outbuf = bytearray()
  outbuf.append(0xaa) 

  for iesc in range(1,len(inbuf)-1):  

    if ( (inbuf[iesc] == 0xaa) or (inbuf[iesc] == 0xab) or (inbuf[iesc] == 0xeb) ):
      outbuf.append(0xeb)
    outbuf.append(inbuf[iesc])

  outbuf.append(0xab)
  return outbuf


def deescape(msgbuf):

  descape = False
  ebaa = b'\xEB\xAA' in msgbuf
  ebab = b'\xEB\xAB' in msgbuf
  ebeb = b'\xEB\xEB' in msgbuf
  if ( (ebaa) or (ebab) or (ebeb) ):
    descape = True  
  msgbuf = msgbuf.replace(b'\xEB\xAA',b'\xAA')
  outbuf = msgbuf.replace(b'\xEB\xAB',b'\xAB')
  outbuf = outbuf.replace(b'\xEB\xEB',b'\xEB')

  return outbuf, descape
