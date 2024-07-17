## Receive SPaT Messages and Manipulate Vehicle Motors

import sys, os
import socket
import binascii
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from math import pi
from time import sleep, time
from threading import Thread


def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def signal_handler(sig, frame):
    print('\nExiting')
    sys.exit(0)  

def getRPM(pwmMot):
    # rpm = int((pwmMot.value-0.083)/(1/240))
    rpm = int((pwmMot.value)/(1/240))
    print("Current RPM: ", rpm)
    return rpm

def getAngVel(pwmMot):
    w = getRPM(pwmMot) * (2*pi/60)
    return w

def getLinSpeed(wheelRad, pwmMot):
    linSp = getAngVel(pwmMot) * wheelRad
    print("Current Speed: ", round(linSp,2))
    return linSp

def distToSig(timeEla, wheelRad, pwmMot):
    dist = round(getLinSpeed(wheelRad, pwmMot) * timeEla, 2)
    return dist


# Motor Declarations
motorSTBY = DigitalOutputDevice(17)
motorA = DigitalOutputDevice(27)
motorB = DigitalOutputDevice(22)
pwmMot = PWMOutputDevice(18)    # pwm pin to control speed
motorSTBY.off()  # initialize motor driver
motorA.on()      # initialize motorA to on for forward direction
motorB.off()     # initialize motorB to off for forward direction

# Listen to broadcast at declared IP + Port
ip_listen = "255.255.255.255"
port_listen = 5005
sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # declare receiving UDP connection
sk_listen.bind((ip_listen, port_listen))

def all():
    # Global Declarations
    global complete
    global linSp

    # Initial Declarations
    dist = int(sys.argv[1])
    totDistance = dist/3.281    # received distance to signal in m
    wheelRad = 0.0365   # radius of wheels in m
    # wheelCir = 2*pi*wheelRad    # wheel circumference in m
    c1tDist = round(totDistance, 2)   # init dist to signal
    timeEla = 0    # initiate time for dist travelled
    distTravelled = 0
    linSp = 0
    complete = 0

    msgIds=['0013'] # this can be updated to include other J2735 PSIDs
    print("Total distance to signal (in meters): ", c1tDist)
    sleep(1)
    print("Vehicle listening.")
    sleep(1)

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
                    # print("Length instersectionPhaseArray: " + str(len(instersectionPhaseArray)))
                    for phase in range(len(instersectionPhaseArray)):
                        currentPhase = decode()['value'][1]['intersections'][0]['states'][phase].get('signalGroup')
                        currentState = str(decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['eventState'])
                        minEndTime = decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['timing']['minEndTime']
                        if (currentPhase == 2):
                            phaseTwo = currentPhase
                            phaseTwoState = currentState
                            timeEndTwo = minEndTime/600
                            # print('Phase: ' + str(currentPhase))
                            # print('  State: ' + currentState)
                        elif (currentPhase == 22):
                            timeEndDouble = minEndTime/600
                    countdown = (timeEndTwo-timeEndDouble)*100
                    print("Time to next state: ", round(countdown,1))

                    if (c1tDist > 0):
                        if (phaseTwoState == "stop-And-Remain" and countdown > 0.5):
                            pwmMot.off()
                            motorSTBY.off()
                            motorA.off()
                            pwmMot = 0
                            timeEla = 0
                            lastStopped = time()
                        else: 
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.value = 0.7
                            timeEla = timeEla + (time() - lastStopped)
                        
                        print('Phase: ', phaseTwoState)
                        print('  State: ', phaseTwo)
                        print("Time elapsed: ", round(timeEla, 2))
                        distTravelled = distTravelled + distToSig(timeEla, wheelRad, pwmMot)
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
except:
    print("Starting thread did not work")
    pwmMot.off()
    motorSTBY.off()
