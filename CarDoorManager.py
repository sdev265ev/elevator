# Original Author: Lonnie Clifton
# Contributors: 
# Date: April 4, 2020
# Revision #: 1.1
# Explanation of Recent Changes: Modified document to follow new coding standards.

# Description of Code: Controls the opening of the car passenger door on arrival at a floor.  Calls CarDoorDriver to interact with the motor.

import time
#import config

def CarDoorManager(Door, action):
	print ("CarDoorManager: Received command: " , action)
	#doorOpenWaitTime = config.doorOpenWaitTime
	doorOpenWaitTime = 3
	while True:
		# Returns when the door is closed.
		#blockedCount = 0
		# If door is open, send the open command if not send the close command.
		if action == 'open':
			print ('CarDoorManager: Sending open command')
			status = Door.moveMotor(1000000)
			print ('CarDoorManager: Status: ', status)
			return 'open'
		
		elif action == 'close':
			print ('CarDoorManager: Sending close command')
			status = Door.moveMotor(-1000000)
			print ('CarDoorManager: Status: ', status)
			return "closed"

		else:
			print ('CarDoorManager: Bad Command')
			return "error"
"""
while CarDoorDriver(Door,'close') == 'blocked':
	# Door is blocked, keep trying to close.
	#blockedCount += 1
	print ('CarDoorManager: Main: Door is blocked')
	print ('CarDoorManager: Sending Open command')
	CarDoorDriver(Door'open')
	print ('CarDoorManager: Waiting for blocked door timeout')
	time.sleep(doorOpenWaitTime)
	print ('CarDoorDriver: Sending close command')
	return "closed"
"""
