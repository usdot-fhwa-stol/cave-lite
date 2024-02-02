## Receive SPaT Messages and Manipulate Vehicle Motors

import signal, sys, os
import socket
import binascii
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from math import pi
from time import sleep, time

def add_asn1_path():
    asn1 = os.path.abspath('..') + "/asn_j2735"
    sys.path.append(asn1)

def signal_handler(sig, frame):
    print('\nExiting')
    sys.exit(0)  

def getRPM():
    # rpm = int((pwmMot.value-0.083)/(1/240))
    rpm = int((pwmMot.value)/(1/240))
    print("Current RPM: ", rpm)
    return rpm

def getAngVel():
    w = getRPM() * (2*pi/60)
    return w

def getLinSpeed():
    linSp = getAngVel() * wheelRad
    print("Current Speed: ", round(linSp,2))
    return linSp

def distToSig(timeEla):
    dist = round(getLinSpeed() * timeEla, 2)
    return dist

# Add ASN.1 to path
add_asn1_path()
import J2735_201603_combined

# Motor Declarations
motorSTBY = DigitalOutputDevice(17)
motorA = DigitalOutputDevice(27)
motorB = DigitalOutputDevice(22)
pwmMot = PWMOutputDevice(18)    # pwm pin to control speed
motorSTBY.off()  # initialize motor driver
motorA.on()     # initialize motorA to on for forward direction
motorB.off()    # initialize motorB to off for forward direction

# Initial Declarations
totDistance = int(sys.argv[1])/3.281    # received distance to signal in m
wheelRad = 0.0365   # radius of wheels in m
# wheelCir = 2*pi*wheelRad    # wheel circumference in m
c1tDist = round(totDistance, 2)   # init dist to signal
timeEla = 0    #initiate time for dist travelled
counter = 0
distTravelled = 0
complete = 0

# listen to broadcast at declared IP + Port
ip_listen = "255.255.255.255"
port_listen = 5005
sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # declare receiving UDP connection
sk_listen.bind((ip_listen, port_listen))


msgIds=['0013'] # this can be updated to include other J2735 PSIDs
print("Total distance to signal (in meters): ", c1tDist)
sleep(1)
print("Vehicle listening.")
sleep(2)
while(complete != 1):
    data = str(sk_listen.recvfrom(10000)[0])
    data = ''.join(data.split())
    # print(data)
    for id in msgIds:
        idx = data.find(id)

        # extract, decode, and use message from stream
        if(idx > -1 ):
            # extract
            if (int('0x'+data[idx+4],16)==8):
                lenstr=int('0x'+data[idx+5:idx+8],16)*2+6 
            else:
                lenstr=int('0x'+data[idx+4:idx+6],16)*2+6
            if (lenstr <= len(data)-idx+1):
                # decode
                msg = data[idx:idx+lenstr].encode('utf-8')
                decode = J2735_201603_combined.DSRC.MessageFrame
                decode.from_uper(binascii.unhexlify(msg))
                # decodedStr = str(decode())
                # print(decodedStr, '\n')

                moy = decode()['value'][1]['intersections'][0]['moy']
                timestamp = decode()['value'][1]['intersections'][0]['timeStamp']
                intersectionID = decode()['value'][1]['intersections'][0]['id']['id']
                intersectionName = decode()['value'][1]['intersections'][0]['name']
                instersectionPhaseArray = decode()['value'][1]['intersections'][0]['states']
                # print("Length instersectionPhaseArray: " + str(len(instersectionPhaseArray)))
                for phase in range(len(instersectionPhaseArray)):
                    currentPhase = str(decode()['value'][1]['intersections'][0]['states'][phase].get('signalGroup'))
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
                    if (c1tDist < totDistance/2):
                        if (phaseTwoState == "protected-Movement-Allowed" and countdown > 2):
                            counter = time()
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.on()
                        elif (phaseTwoState == "stop-And-Remain" and countdown > 3):
                            if (c1tDist < totDistance/4):
                                counter = 0
                                motorA.on()
                                pwmMot.off()
                                motorSTBY.off()
                            else:
                                counter = 0
                                pwmMot.off()
                                motorA.off()
                                motorSTBY.off()
                        elif (phaseTwoState == "protected-clearance" and countdown > 1):
                            if (c1tDist > totDistance/4):
                                counter = time()
                                motorSTBY.on()
                                motorA.on()
                                pwmMot.value = .6
                            else:
                                counter = time()
                                motorSTBY.on()
                                motorA.on()
                                pwmMot.value = .7
                    else:
                        if (phaseTwoState == "protected-Movement-Allowed" and countdown > 2):
                            counter = time()
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.on()
                        elif (phaseTwoState == "protected-clearance"):
                            counter = time()
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.off()
                        elif (phaseTwoState == "stop-And-Remain" and countdown > 3):
                            counter = 0
                            pwmMot.off()
                            motorSTBY.off()
                            motorA.off()
                        elif (phaseTwoState == "stop-And-Remain" and countdown < 2):
                            counter = time()
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.value = 0.6
                        else: 
                            counter = time()
                            motorSTBY.on()
                            motorA.on()
                            pwmMot.value = 0.7

                    # timeEla = time() - initTime # calculate time elapsed since init vehicle move
                    # print("Time since init movement: ", round(timeEla, 1))
                    if (counter == 0):
                        timeEla = timeEla
                    else:
                        timeEla = timeEla + (time() - counter)
                    
                    print('Phase: ' + phaseTwoState)
                    print('  State: ' + phaseTwo)
                    # print("Time elapsed: ", round(timeEla,2))
                    distTravelled = distTravelled + distToSig(timeEla)
                    print("Distance Travelled: ", round(distTravelled,2))
                    c1tDist = round(totDistance - distTravelled)
                    print("C1T distance to signal: ", round(c1tDist,2))

                else:
                    pwmMot.off()
                    motorA.off()
                    motorSTBY.off()
                    complete = 1
                break



signal.signal(signal.SIGINT, signal_handler)
motorSTBY.off()
print('\nPress Ctrl+C to exit')
signal.pause()
