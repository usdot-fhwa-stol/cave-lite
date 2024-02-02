## Receive, Decode, Broadcast SAE J2735 Messages

import os
import os.path
import sys
import socket
import binascii
import datetime
from time import sleep
from threading import Thread
# from gpiozero import LED  # uncomment if physical digital signal head will be used

def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def send(ip_send, port_send, msg, broadcast):
    sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk_send.bind((ip_send, 0))
    sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
    sk_send.sendto(msg, (broadcast, port_send)) # broadcast message
    sk_send.close()

def writePhase(phase): 
    # fout.writelines(["Phase ", str(phase), ': '])
    print("Phase ", str(phase), ': ')

def writeState(state):
    # fout.writelines([str(state),  "\n"])
    print(str(state),  "\n")

def writeTime(seconds, millisec):
    global countdown
    countdown = round(seconds-millisec, 1)
    # fout.writelines(["Time to next state: ", str(countdown), "\n"])
    print("Time to next state: ", str(countdown), "\n")

def writeLog():
    path = os.getcwd() + "/logs/"
    stamp = str(datetime.datetime.now())
    timestamp = stamp.replace("-", "_")
    timestamp = timestamp.replace(" ", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(".", "")
    logPath = os.path.join(path, timestamp+".log")
    fout = open(logPath, 'w')
    return fout

## uncomment to declare LED pins and set initial states for signal head hardware
# red = LED(17)
# yellow = LED(27)
# green = LED(22)
# red.on()
# yellow.off()
# green.off()

# Declarations
print('Starting intersect.')
ip_listen = '127.0.0.1'
ip_send = '192.168.0.255'
broadcast = '255.255.255.255'
port_listen = 1516 # listen to Immediate Forward Plugin
port_send = 5005
sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk_listen.bind((ip_listen, port_listen))
updatingState = None
countdown = None

## uncomment all fout.* to write logs
# fout = writeLog()

msgIds=['0013'] # this can be updated to include other J2735 PSIDs
print("Waiting to receive data\n")
def all():
    global updatingState
    while(1):
        data = str(sk_listen.recvfrom(10000)[0])
        data = ''.join(data.split())
        for id in msgIds:
            idx = data.find(id)
            
            ## extract, decode, and send message from stream
            if(idx > -1 ):
                ## extract
                if (int('0x'+data[idx+4],16)==8):
                    lenstr=int('0x'+data[idx+5:idx+8],16)*2+6 
                else:
                    lenstr=int('0x'+data[idx+4:idx+6],16)*2+6
                if(lenstr <= len(data)-idx+1):
                    ## decode
                    msg = data[idx:idx+lenstr].encode('utf-8')
                    decode = J2735_201603_combined.DSRC.MessageFrame
                    decode.from_uper(binascii.unhexlify(msg))

                    instersectionPhaseArray = decode()['value'][1]['intersections'][0]['states']
                    for phase in range(len(instersectionPhaseArray)):
                        currentPhase = decode()['value'][1]['intersections'][0]['states'][phase].get('signalGroup')
                        currentState = str(decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['eventState'])
                        minEndTime = decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['timing']['minEndTime']
                        if (currentPhase == 2) : # additional phases may be included as the same if-statements
                            writeState(currentState)
                            writePhase(currentPhase)
                            timeEndSec = minEndTime/6
                            print("timeEndSec: ", timeEndSec*6)
                            updatingState = currentState
                        elif (currentPhase == 22) :
                            timeEndMilliSec = minEndTime/6
                            print("timeEndMilliSec: ", timeEndMilliSec*6)
                    writeTime(timeEndSec, timeEndMilliSec)

                    ## send
                    send(ip_send, port_send, msg, broadcast)
                    sleep(0.1)

try:
    add_asn1_path()
    import J2735_201603_combined
    
    t = Thread(target = all, args=(),  daemon = True) 
    t.start()
except:
    print("Starting thread did not work")
