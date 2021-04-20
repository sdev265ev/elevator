# Original Author: Lonnie Clifton
# Contributors: 
# Date: April 5, 2020
# Revision #: 1.1
# Explanation of Recent Changes: Modified document to follow new coding standards.

# Description of Code: This module contains global identifiers and common functions to be imported into modules.

#!/usr/bin/python

import socket
import datetime
import time

Role = "" # Hall or Master.

# =================== Lift Values.
# Top floor and bottom floor created as variables to allow for changing sizes.

TopFloor = 5
BottomFloor = 1
FloorStopList    = []
CarFloorStopList = []
StopNow = False

# Lift Motor BCM pin numbers.
#CarLampsPins  = [0,19,20,21,22,23]
#CarButtonPins = [0,14,15,16,17,18]
#LSBottomPin   = 7
#LSTopPin      = 8

# Lift Motor BOARD pin numbers.
CarLampsPins  = [0,35,38,40,15,16]
CarButtonPins = [0,8,10,36,11,12]
LSBottomPin   = 7
LSTopPin      = 8

CarStepWaitTime = .0012

# ========================Lift Door Motor Values 



# ============== Master Controller.
MasterIpAddress = "0"
MasterPortAddress = 5005
StopMetricsDictionary = {}

# Dictionary created to relate IP address to car.
HallCarDictionary = {}
hallCallsUP   = [0,0,0,0,0,0]
hallCallsDOWN = [0,0,0,0,0,0]

def send(message, ip, port = 5005):
	#print ('config.Send: ', ip)
	messageBytes = message.encode() # Message is broken down into bits to be transmitted over the internet.
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.sendto(messageBytes, (ip, port))
	#sock.sendto(message.encode(), (ip, port))

DEBUGLEVEL = 0
#This is a generic logging function. 
#  Can be updated to send messages to a file or database
def logThis(source, message, level = 1):
	if level > DEBUGLEVEL:
		dt = str(datetime.datetime.now())
		msg = dt  + " | " + source + " | " + message 
		print (msg)
