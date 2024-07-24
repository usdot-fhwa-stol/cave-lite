## Receive SPaT Messages and Manipulate Vehicle Motors

import sys, os
import socket
import binascii
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from math import pi
import time
from threading import Thread, Lock

linSp = 0  # Initialize linSp at the module level
linSp_lock = Lock()  # A lock to ensure thread-safety when updating linSp

def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def getRPM(pwmVal):
    rpm = int((pwmVal)/(1/240))
    print("Current RPM: ", rpm)
    return rpm

def getAngVel(pwmVal):
    w = getRPM(pwmVal) * (2*pi/60)
    return w

def getLinSpeed(wheelRad, pwmVal):
    global linSp
    with linSp_lock:  # Use the lock when updating linSp
        linSp = getAngVel(pwmVal) * wheelRad
        print("Current Speed: ", round(linSp, 2))
    return linSp

def distToSig(timeEla, wheelRad, pwmVal):
    dist = round(getLinSpeed(wheelRad, pwmVal) * timeEla, 2)
    return dist

def countdown(endTime, currentSec, currentDecSec):
    currentTime = currentSec + currentDecSec / 10.0
    countdown = round(endTime - currentTime, 2)
    print("Time to next state: {:.1f}".format(countdown))

def all():
    # Global Declarations
    global complete

    # Motor Declarations
    motorSTBY = DigitalOutputDevice(17)
    motorA = DigitalOutputDevice(27)
    motorB = DigitalOutputDevice(22)
    pwmMot = PWMOutputDevice(18)    # pwm pin to control speed
    motorSTBY.off()  # initialize motor driver
    motorA.on()      # initialize motorA to on for forward direction
    motorB.off()     # initialize motorB to off for forward direction

    # Initial Declarations
    dist = int(sys.argv[1])
    totDistance = dist/3.281    # received distance to signal in m
    wheelRad = 0.0365   # radius of wheels in m
    c1tDist = round(totDistance, 2)   # init dist to signal
    timeEla = 0    # initiate time for dist travelled
    distTravelled = 0
    complete = 0
    lastTime = time.time()

    # Listen to broadcast at declared IP + Port
    ip_listen = "255.255.255.255"
    port_listen = 5005
    sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # declare receiving UDP connection
    sk_listen.bind((ip_listen, port_listen))

    msgIds=['0013'] # this can be updated to include other J2735 PSIDs
    print("Total distance to signal (in meters): ", c1tDist)
    print("Vehicle listening.")
    time.sleep(1)

    while(complete != 1):
        data = str(sk_listen.recvfrom(10000)[0])
        data = ''.join(data.split())
        # print(data)
        for id in msgIds:
            idx = data.find(id)

            ## extract, decode, and use message from stream
            if(idx > -1 ):
                ## extract
                if (int('0x'+data[idx+4],16)==8):
                    lenstr=int('0x'+data[idx+5:idx+8],16)*2+6 
                else:
                    lenstr=int('0x'+data[idx+4:idx+6],16)*2+6
                if (lenstr <= len(data)-idx+1):
                    ## decode
                    msg = data[idx:idx+lenstr].encode('utf-8')
                    decode = J2735_201603_combined.DSRC.MessageFrame
                    decode.from_uper(binascii.unhexlify(msg))
                    # decodedStr = str(decode())
                    # print(decodedStr, '\n')

                    instersectionPhaseArray = decode()['value'][1]['intersections'][0]['states']
                    utcTime = time.gmtime()
                    utcMin = utcTime.tm_min
                    utcSec = utcTime.tm_sec
                    utcDeci = int((time.time()%1) * 10)
                    currentSec = utcMin*60 + utcSec
                    for phase in range(len(instersectionPhaseArray)):
                        currentPhase = decode()['value'][1]['intersections'][0]['states'][phase].get('signalGroup')
                        currentState = str(decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['eventState'])
                        minEndTime = decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['timing']['minEndTime']
                        if (currentPhase == 2):
                            phaseTwo = currentPhase
                            phaseTwoState = currentState
                            timeEndTwo = minEndTime/10
                    countdown(timeEndTwo, currentSec, utcDeci)

                    if (c1tDist > 0):
                        if (phaseTwoState == "stop-And-Remain"):
                            pwmMot.off()
                            pwmVal = 0
                            motorSTBY.off()
                            motorA.off()
                            timeEla = 0
                            lastTime = time.time()
                        else: 
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.value = 0.3
                            pwmVal = 0.3
                            timeEla = time.time() - lastTime

                        print('Phase: ', phaseTwoState)
                        print('  State: ', phaseTwo)
                        print("Time elapsed: ", round(timeEla, 2))
                        distTravelled = distTravelled + distToSig(timeEla, wheelRad, pwmVal)
                        print("Distance Travelled: ", round(distTravelled, 2))
                        c1tDist = round(totDistance - distTravelled)
                        print("Vehicle distance to signal: ", round(c1tDist, 2))

                    else:
                        pwmMot.off()
                        motorA.off()
                        motorSTBY.off()
                        complete = 1
                        print("Vehicle destination reached.")
                    break


try:
    add_asn1_path()
    import J2735_201603_combined

    t = Thread(target = all, args=(),  daemon = True) 
    t.start()
except Exception as e:
    print(f"Starting thread did not work: {e}")
