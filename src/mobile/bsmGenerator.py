# BSM Generator
from threading import Thread
import socket, sys, os
import binascii as ba
import datetime
from time import sleep
from binascii import hexlify
import msgRecv

def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def send(ip_send, port_send, bsm, broadcast):
    sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk_send.bind((ip_send, 0))
    sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
    sk_send.sendto(bsm, (broadcast, port_send)) # broadcast message
    sk_send.close()

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
    global speed
    speed = int(msgRecv.linSp*20)
    print(speed)
    return speed

def encode(bsmDict):
    msgFrame = J2735_201603_combined.DSRC.MessageFrame
    msgFrame.set_val(bsmDict)
    msgFrameUper = msgFrame.to_uper()
    encodedBSM = hexlify(msgFrameUper)
    print(encodedBSM)
    return encodedBSM

def main():
    # Continually update values in dict and encode:
    bsm = {'messageId': 20, 'value': ('BasicSafetyMessage', {'coreData': {'msgCnt': 18, 'id': b'g\xc9_l', 'secMark': 28782, 'lat': 389548850, 'long': -771483730, 'elev': 394, 'accuracy': {'semiMajor': 255, 'semiMinor': 255, 'orientation': 65535}, 'transmission': 'forwardGears', 'speed': 234, 'heading': 28800, 'angle': 127, 'accelSet': {'long': 2001, 'lat': 2001, 'vert': -127, 'yaw': 32767}, 'brakes': {'wheelBrakes': (0, 5), 'traction': 'unavailable', 'abs': 'unavailable', 'scs': 'unavailable', 'brakeBoost': 'unavailable', 'auxBrakes': 'unavailable'}, 'size': {'width': 0, 'length': 0}}})}
    msgCount = 0
    global encoded_bsm

    # Declarations:
    ip_send = '192.168.0.255'
    broadcast = '255.255.255.255'
    port_send = 26789

    print("Broadcasting messages.")
    print("Press Ctrl+C to exit.")

    while(1):
        msgCount = getMsgCount(msgCount)
        bsm['value'][1]['coreData']['msgCnt']  = msgCount
        bsm['value'][1]['coreData']['secMark'] = getSecMark()
        bsm['value'][1]['coreData']['speed']   = getSpeed()

        data = encode(bsm)
        unhexed = ba.unhexlify(data)
        send(ip_send, port_send, unhexed, broadcast)
        sleep(0.1) # sleep to generate a new BSM every 0.1 seconds


if __name__ == '__main__':
    add_asn1_path()
    import J2735_201603_combined
    sys.exit(main())
