# Original Author: Lonnie Clifton
# Contributors: 
# Date: April 4, 2020
# Revision #: 1.1 
# Explanation of Recent Changes: Modified document to follow new coding standards.

# Description of Code: Controls direction of elevator cars based on calls received.

# TODO:
#   add comments at top of this module the describe the purpose of this module
#   Describe reason for the StepperDriverClass
#   Add recommendations for identifier names
# pip3 install keyboard

# sudo python3 -m pip install keyboard
# import keyboard  # using module keyboard (must use apt-get)
import time
import config
import RPi.GPIO as GPIO

from StepperDriverClass import StepperDriverClass
import CarLampManager as clm
import CarButtonCallBack
import CarButtonInitialize
import CarLampInitialize
import CarDoorManager  as cdm
import CarFindMaster   as cfm
import NetworkListener as nl

import socket
# Generic method to send a text message to the ip address in the method.
#  All information sent must be changed (encoded) to byte code
def send(message, ip, port = 5005):
	#print ('Send: ', ip, port)
	messageBytes = message.encode() 				# message is encoded into byte code for transmission
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 	# a socket datagram is the UDP protocol
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# This was found to be needed to avoid running out of buffer space
	sock.sendto(messageBytes, (ip, port))
	#sock.sendto(message.encode(), (ip, port))			# Altermate code, above appears to be somewhat simpler

def UpdateMaster(stoplist):
	# We cannot send an object such as a list object, over the network and be understood 
	# there is a better algorithm to convert to a csv string.
	stringList = 'arrived@floor:'		# header to identify the data purpose
	
	# Convert list to CSV string for network transmission.
	stringList += str(stoplist[0]) # Index. 
	for f in range(1, len(stoplist)):
		stringList += ','
		stringList += str(stoplist[f])
	#print ('UpDateMaster - SendStopList: stringList: ', stringList)
	send(stringList, config.MasterIpAddress)
"""
	# Better method
	myList = [1,2,3,4]]
	s=str(myList)
	print (s)
	s= s.replace('[', '')
	s= s.replace(']', '')
	s= s.replace(' ' , '')
	print (s)
	#This is the code for to change to a list object
	ss = list(s.split( ','))		# creates a list of characters
	print (ss)
	myNewList = list(map(int, ss))		# remap into as list of numbers
	print (myNewList)
"""
	
def CarManager():
	topFloor = config.TopFloor
	bottomFloor = config.BottomFloor
	totalSteps = 0

	CarLampInitialize.CarLampInitialize() # Configure GPIO and turn off car lamps.
	CarButtonInitialize.CarButtonInitialize() # Set the car buttons for callbacks	.

	# The stepper driver is a class. Create an instance for the lift stepper motor and one for the door stepper motor.
	Car = StepperDriverClass(id, [31,29,7,5], 26, 24 ) # Create an instance of the stepper motor driver.
	Door = StepperDriverClass(id, [37,22,19,21], 32, 23 ) # Create an instance of the stepper motor driver.
	
	#cycle door and leave open (we start on the bottom floor
	#print ('CarManager: Cycling door')
	#cdm.CarDoorManager(Door, 'open')
	#time.sleep(1)
	#cdm.CarDoorManager(Door, 'close')
	#print ('CarManager: Door Cycling Completed')
		
	#  Set the floor stop list to the proper size per the configuration
	config.CarFloorStopList = [0] * (config.TopFloor + 1) # Create floor stop list, need one more for zero index.
	config.CarFloorStopList[0] = 1 # Set car location to 1 going up.
	
	# To work in a multi-elevator environment, we need to tell the master controller of this elevator posiion and direction
	#  The IP address of the master controller is stored in the configuration file
	cfm.GetMasterIP() # Get the IP address of the Master controller.
	
	# This call will start a separate thread that will listen to commands from the master controller
	nl.udpListenerMain()
	
	
	# Begin car intialization to find the stepper motor steps required to move the car to the top floor
	# Bottom floor is like a reference position
	print ('CarManager: Moving to bottom floor')
	Car.moveMotor(-1000000)
	time.sleep(.5)
	
	print ('CarManager: Moving to top floor to count steps')
	# Will stop when car reaches limit switch.
	totalSteps = Car.moveMotor(1000000)
	
	#the total steps is a measure of the distance from the bottom to the top floor
	#  Used to find the number of steps to a given floor (no detection device at each floor)
	print ("CarManager: Total steps: ", totalSteps)
	time.sleep(1)		# Pause may not be needed
		
	#print ('CarManager: Moving to bottom floor')
	Car.moveMotor(-1000000)
		
	# Setting parameters for directions, height (in steps) of elevator, and initial floor.
	floor = 1
	direction = 1
	stepsPerFloor = totalSteps / (topFloor - 1)
	
	# tell the master controller where this car is currently loacated (which will be on the current floor)
	UpdateMaster(config.CarFloorStopList)
	
	# ====================== MAIN LOOP ===============================
	print ('CarManager: Starting main loop')
	currentFloor = 1

	while True:
		# Poll the floor stop list continuously.
		# The floor poll will look ahead for floors to stop at.
		# If a floor stop is found, the car is "pulled" to that floor - up or sown.
		# Along the way,  at each floor is checked to see if a new stop has come in,
		#    either from inside the car or from the master controller.

		# This is the beginning of experimental code to allow calling a floor from the keyboard
		#if keyboard.is_pressed('1'):  # if key '1' is pressed 
		#	CarButtonCallBack(1)
		#elif keyboard.is_pressed('2'):  # if key '2' is pressed 
		#	CarButtonCallBack(2)
		#elif keyboard.is_pressed('3'):  # if key '3' is pressed 
		#	CarButtonCallBack(3)
		#elif keyboard.is_pressed('4'):  # if key '4' is pressed 
		#	CarButtonCallBack(4)
		#elif keyboard.is_pressed('5'):  # if key '5' is pressed 
		#	CarButtonCallBack(5)

		if config.CarFloorStopList[floor] == 1:
			# We are scanning the call list looking for a floor call (floor =  1 value)
			# We must physically move the car to this floor
			# The floor being checked may not be where the car is actually currently located.
			# It may be above or below the checked floor.
			#cdm.CarDoorManager(Door, 'close')
			while currentFloor != floor:
				# Move the car until a stop floor is reached.
				if (floor - currentFloor) > 0:
					# Move car up toward logical floor.
					moveDirection = 1
				else:
					#  otherwise we new o move it downward
					moveDirection = -1

				# Wait for the door to close
				Car.moveMotor(stepsPerFloor * moveDirection)		# Move one floor.
				currentFloor += moveDirection				# Now moved, update floor.
				config.CarFloorStopList[0] = currentFloor * direction	# Update list for new floor and direction.
			config.CarFloorStopList[currentFloor] = 0			# Clear list entry for this floor.
			clm.CarLampManager(currentFloor, 0) 				# Car lamp turned off for this floor
			UpdateMaster(config.CarFloorStopList)				# Tell master the floor where now located
	
		#cdm.CarDoorManager(Door, 'open')					# Stopped at floor
		# time.sleep(3)
		#cdm.CarDoorManager(Door, 'close')		
		floor += direction							# next floor - up or down
		
		# Change direction if top or bottom floor reached.
		if floor > topFloor - 1:
			direction = -1
		if floor < bottomFloor + 1: 
			direction = 1
		time.sleep(1)
