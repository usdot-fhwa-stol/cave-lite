# BSM Generator
from threading import Thread
import sys, os
import datetime
from time import sleep
from binascii import hexlify
import msgRecv

def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def getMsgCount(msgCount):
    msgCount += 1
    if (msgCount == 128):
        msgCount = 1
    return int(msgCount)

def getSecMark():
    time = str(datetime.datetime.now())
    time = float(time.split(':')[2])
    secMark = str((time*1000)%60000).split('.')[0]
    return int(secMark)

def getSpeed():
    with msgRecv.linSp_lock:  # Ensure thread-safety
        speed = int(msgRecv.linSp * 20)
    return speed

def encode(bsmDict):
    msgFrame = J2735_201603_combined.DSRC.MessageFrame
    msgFrame.set_val(bsmDict)
    msgFrameUper = msgFrame.to_uper()
    encodedBSM = hexlify(msgFrameUper)
    return encodedBSM

encoded_bsm = None  # Initialize the global variable

def all():
    # Global Declaration
    global encoded_bsm

    # Continually update values in dict and encode:
    bsm = {'messageId': 20, 'value': ('BasicSafetyMessage', {'coreData': {'msgCnt': 18, 'id': b'g\xc9_l', 'secMark': 28782, 'lat': 389548850, 'long': -771483730, 'elev': 394, 'accuracy': {'semiMajor': 255, 'semiMinor': 255, 'orientation': 65535}, 'transmission': 'forwardGears', 'speed': 234, 'heading': 28800, 'angle': 127, 'accelSet': {'long': 2001, 'lat': 2001, 'vert': -127, 'yaw': 32767}, 'brakes': {'wheelBrakes': (0, 5), 'traction': 'unavailable', 'abs': 'unavailable', 'scs': 'unavailable', 'brakeBoost': 'unavailable', 'auxBrakes': 'unavailable'}, 'size': {'width': 0, 'length': 0}}})}
    msgCount = 0

    while True:
        msgCount = getMsgCount(msgCount)
        bsm['value'][1]['coreData']['msgCnt']  = msgCount
        bsm['value'][1]['coreData']['secMark'] = getSecMark()
        bsm['value'][1]['coreData']['speed']   = getSpeed()

        encoded_bsm = encode(bsm)
        sleep(0.1) # sleep to generate a new BSM every 0.1 seconds

try:
    add_asn1_path()
    import J2735_201603_combined
    
    t = Thread(target = all, args=(),  daemon = True) 
    t.start()
except Exception as e:
    print(f"Starting thread did not work: {e}")
