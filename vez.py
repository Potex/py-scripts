#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Sept 3 14:55:40 2018
@author: Potex (github.com/Potex)
Python version: 3.4.2

Vezérlő script távirányításhoz készítve.
"""

# Raspberry Pi script which sends recieves UDP packets
# API reference: https://github.com/horverno/deep-pilot/wiki/API-reference **** NEEDS UPDATE *****

import serial
import socket
import json
import threading
import time
            
udpIp = "192.168.0.105" #"255.255.255.255" # broadcast
udpPortRead = 5006
udpPortSend = 5005
exitFlag = False
sendDict = {"Time": 0}
sendDelay = 1 # 1 Hz by default

motSetSpeedSigRefDrive = '1.00'
motSetAngRefSteering= '1.00'

sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sockR.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # UDP
sockR.bind(('', udpPortRead)) # UDP
sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

ser=serial.Serial("/dev/ttyACM0", 115200)

Feedbackread = ""

#time.sleep(6)
#ser.flushInput()  

##motorSpeed = '1.00'
##servoPosStr ='1.00'

def motorControl():
    global exitFlag, idMotDrive, idMotSteering, motSpeedDrive, motPosDrive, motPosSteering, motSetSpeedSigRefDrive, motLoadDrive
    while not exitFlag:
        ser.flushInput()
        messageList = [motSetSpeedSigRefDrive, motSetAngRefSteering]
        MessageStringStr = ','.join(messageList)+'a'
        print(MessageStringStr)
        ser.write(MessageStringStr.encode('ascii'))
        time.sleep(0.1)
        #ProbaStr = "1.0,1.0a"
        #print(ProbaStr)
        #ser.write(ProbaStr.encode('ascii'))
    print(" >> motorControl thread stopped.")

def feedbackInfo():
    global exitFlag, feedbackRead
    while not exitFlag:
        feedbackRead = ser.readline()
        print (feedbackRead)
    print(" >> feedbackInfo thread stopped.")    

def sendMsg():
    global exitFlag, sendDelay, sendDict, idMotSteering, idMotDrive, motSpeedDrive, feedbackRead
    startTime = time.time()
    #print(" >> Write message thread started.")
    while not exitFlag:
        time.sleep(sendDelay)
        elapsedTime = time.time() - startTime
        sendDict["Time"] = elapsedTime
        print(elapsedTime)
	sendDict["FeedBack"] = feedbackRead
        sockS.sendto((json.dumps(sendDict)).encode('ascii'), (udpIp, udpPortSend))
    print(" >> Write message thread stopped.")

def readMsg():
    global exitFlag, udpIp, sendDelay, sendDict, motSetSpeedSigRefDrive, motSetAngRefSteering, 
    #print("Read message thread started.")
    while not exitFlag:
        readData, addr = sockR.recvfrom(1024) # buffer size
        try:
            readDict = json.loads(str(readData,'utf-8'))
            for d in readDict:
                if("Exit" == d):
                    exitFlag = True
                elif("SetUdpIpSend" == d):
                    udpIpSend = readDict["SetUdpIpSend"]
                    print("New ip: %s" % (udpIpSend))
                elif("SetDelay" == d):
                    sendDelay = float(readDict["SetDelay"])
                    print(" >> New frequency: %.2f" % (1 / sendDelay))
                elif("SetSpeedSignalReferenceDrive" == d):
                    motSetSpeedSigRefDrive = readDict["SetSpeedSignalReferenceDrive"]
                    print(" >> New vehicle speed: %s" % (readDict["SetSpeedSignalReferenceDrive"]))
                elif("SetAngleReferenceSteering" == d):
                    motSetAngRefSteering = readDict["SetAngleReferenceSteering"]
                    print(" >> New steering angle: %s" % (readDict["SetAngleReferenceSteering"]))          
                '''elif("SendMotorPositionDrive" == d):
                    if readDict["SendMotorPositionDrive"] == True:
                        sendDict["MotorPositionDrive"] = 0
                        print(" >> Sending motor position too...")
                    else:
                        try:
                            del sendDict["MotorPositionDrive"]
                            break
                        except:
                            print(" >> Error deleting MotorPositionDrive")
                        print(" >> Stopped sending motor position...")
                elif("SendMotorSpeedDrive" == d):
                    if readDict["SendMotorSpeedDrive"] == True:
                        sendDict["VehicleSpeedDyna"] = 0
                        print(" >> Sending motor speed (VehicleSpeedDyna) too...")
                    else:
                        try:
                            del sendDict["VehicleSpeedDyna"]
                            break
                        except:
                            print(" >> Error deleting VehicleSpeedDyna")
                        print(" >> Stopped sending motor position...")         
                elif("SendMotorLoadDrive" == d):
                    if readDict["SendMotorLoadDrive"] == True:
                        sendDict["MotorLoadDrive"] = motLoadDrive
                        print(" >> Sending motor load (MotorLoadDrive) too...")
                    else:
                        try:
                            del sendDict["MotorLoadDrive"]
                            break
                        except:
                            print(" >> Error deleting MotorLoadDrive")
                        print(" >> Stopped sending motor load...")         
                '''
                else:
                    print("R: %s not recognized" % str(readData,'utf-8'))
        except:
            print(" >> Not valid JSON sting recieved.")
    print(" >> Read message thread stopped.")

# main

print("Listening... (waiting for exit message)")

s = threading.Thread(target=sendMsg)
r = threading.Thread(target=readMsg)
m = threading.Thread(target=motorControl)
f = threading.Thread(target=feedbackInfo)
s.start()
r.start()
m.start()
f.start()
s.join() # block until all tasks are done
r.join() # block until all tasks are done
m.join() # block until all tasks are done
f.join() # block until all tasks are done

ExitStr = "1.0,1.0a"
ser.write(ExitStr.encode('ascii'))
time.sleep(0.1)
ser.close()
print("Exit message recieved. Serial connection closed, motor stopped, steering set to middle position. ")
