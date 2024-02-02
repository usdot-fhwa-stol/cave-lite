# BSM Generator
import signal, sys, os
import datetime
import ast
from time import sleep
from binascii import hexlify
from msgRecv import getLinSpeed

def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def signal_handler(sig, frame):
    print('\nExiting')
    sys.exit(0)

def getMsgCount():
    oldMsgCount = msgCount
    msgCount += 1
    if (msgCount == 128):
        msgCount = 0
    return int(oldMsgCount)

def getSecMark():
    time = str(datetime.datetime.now())
    time = float(time.split(':')[2])
    secMark = str((time*1000)%60000).split('.')[0]
    return secMark

def getSpeed():
    speed = int(getLinSpeed()*20)
    return speed

def encode():
    msgFrame = J2735_201603_combined.DSRC.MessageFrame
    msgFrame.set_val(bsmDict)
    msgFrameUper = msgFrame.to_uper()
    encodedBSM = hexlify(msgFrameUper)
    return encodedBSM

# read contents of bsmFrame.txt file
fout = open("bsmFrame.txt", 'r')
bsm = fout.readline()
bsmDict = ast.literal_eval(bsm) # convert file contents to dictionary
fout.close()

add_asn1_path()
import J2735_201603_combined

# continually update values in dict and encode
while(1):
    bsmDict['value'][1]['coreData']['msgCnt']  = getMsgCount()
    bsmDict['value'][1]['coreData']['secMark'] = getSecMark()
    bsmDict['value'][1]['coreData']['speed']   = getSpeed()

    encode()
    sleep(0.1) # generates a new BSM every 0.1 seconds, per SAE J2735

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
