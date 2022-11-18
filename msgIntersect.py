# Receive, Decode, Broadcast SAE J2735 Messages
import J2735_201603_combined
import signal, sys
import os.path
import socket
import binascii
from time import sleep
# from gpiozero import LED
import datetime
# import trafficSignal


def send(ip_send, port_send, msg, broadcast):
    sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk_send.bind((ip_send, 0))
    sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
    sk_send.sendto(msg, (broadcast, port_send)) # broadcast message
    sk_send.close()

def writePhase(phase): 
    fout.writelines(["Phase ", str(phase), ': '])
    return None

def writeState(currentState):
    phaseTwoState = currentState
    fout.writelines([str(phaseTwoState),  "\n"])
    return phaseTwoState

def writeLog():
    path = '/home/willdesk/Documents/cave-lite/logs/' # '/home/cave/cave-lite/logs/'
    stamp = str(datetime.datetime.now())
    timestamp = stamp.replace("-", "_")
    timestamp = timestamp.replace(" ", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(".", "")
    logPath = os.path.join(path, timestamp+".log")
    fout = open(logPath, 'w')
    return fout

# def signalOut(phaseState):
#     state = phaseState
#     print("In signalOut\n")
#     if (state() == "stop-And-Remain") :
#         print("red\n")
#         object.self.C.delete(object.self.greenLight)
#         object.self.light["1"].setRed()
#     elif (state() == "protected-clearance") :
#         print("yellow\n")
#         object.self.C.delete(object.self.redLight)
#         object.self.light["1"].setYellow()
#     elif (state() == "protected-Movement-Allowed") :
#         print("green\n")
#         object.self.C.delete(object.self.yellowLight)
#         object.self.light["1"].setGreen()
#     else: object.self.light["1"].setRed()

# object = trafficSignal.intersection(top)

# uncomment to declare LED pins and set initial states for traffic light hardware
# red = LED(17)
# yellow = LED(27)
# green = LED(22)
# red.on()
# yellow.off()
# green.off()

print('Starting intersect.')
ip_listen = '192.168.0.156'
ip_send = '192.168.0.255'
broadcast = '255.255.255.255'
port_listen = 1516 # listen to Immediate Forward Plugin
port_send = 5005
sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # declare receiving UDP connection
sk_listen.bind((ip_listen, port_listen))

fout = writeLog()

msgIds=['0013'] # this can be updated to include other J2735 PSIDs
print("Receiving Data")
while(1):
    data = str(sk_listen.recvfrom(10000)[0])
    data = ''.join(data.split())
    # print(data)
    for id in msgIds:
        idx = data.find(id)
        # extract, decode, and send message from stream
        if(idx > -1 ):
            # extract
            if (int('0x'+data[idx+4],16)==8):
                lenstr=int('0x'+data[idx+5:idx+8],16)*2+6 
            else:
                lenstr=int('0x'+data[idx+4:idx+6],16)*2+6
            if(lenstr <= len(data)-idx+1):
                # decode
                msg = data[idx:idx+lenstr].encode('utf-8')
                decode = J2735_201603_combined.DSRC.MessageFrame
                decode.from_uper(binascii.unhexlify(msg))
                # decodedStr = str(decode())
                # print(decodedStr, '\n')

                instersectionPhaseArray = decode()['value'][1]['intersections'][0]['states']
                for phase in range(len(instersectionPhaseArray)):
                    currentPhase = decode()['value'][1]['intersections'][0]['states'][phase].get('signalGroup')
                    currentState = str(decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['eventState'])
                    minEndTime = decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['timing']['minEndTime']
                    if (currentPhase == 2) : # additional phases may be included as the same if-statements
                        writeState(currentState)
                        writePhase(phase)
                        timeEndSec = minEndTime/600
                    elif (currentPhase == 22) :
                        timeEndDouble = minEndTime/600
                    
                countdown = (timeEndSec-timeEndDouble)*100
                fout.writelines(["Time to next state: ", str(round(countdown,1)), "\n"])

                send(ip_send, port_send, msg, broadcast)
                sleep(0.1)
                break