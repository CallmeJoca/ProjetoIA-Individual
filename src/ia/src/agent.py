#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Jorge Pissarra, a39489
import math
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from itertools import chain
from operator import itemgetter

x_ant = 0
y_ant = 0
obj_ant = ''

current_position = [0, 0] # keep track of the position of the agent
previous_room = 0         # keep track of the room/corridor the agent just left
current_room = 1          # keep track of the room/corridor the agent is in

Rooms = [["0", "generic room"] for _ in range(14)] # generate a list of lists: each sub-list contains the number, type and objects from each room
Rooms[0].insert(0, str(current_room))              # update the first element with the number of the first room, that being corridor 1
Rooms[0].remove("0")							   # remove the extra element created by the above instruction
Rooms[0].insert(1, "corridor")					   # update the first element with the room type of the first room, that being corridor 1
Rooms[0].remove("generic room")					   # remove the extra element created by the above instruction

Suites = []	# create a list to hold each pair of rooms that make up a suite

Single_rooms = [[0,0,0]] # create a list of lists to hold the room number and central coordinates of each single room

def getRoomCenter(i): # function that returns the central coordinates of each room
	if i == 5:
		return -14.0, 0.7
	elif i == 6:
		return -14.0, 5.1
	elif i == 7:
		return -14.0, 9.5
	elif i == 8:
		return -8.2, 9.5
	elif i == 9:
		return -3.4, 9.5
	elif i == 10:
		return 1.5, 9.5
	elif i == 11:
		return 1.4, 3.6
	elif i == 12:
		return 1.4, 2.2
	elif i == 13:
		return -8.0, 3.8
	elif i == 14:
		return -5.5, 3.8

def room_coordinates(x,y): # function that returns the room number in function of the current position of the agent
	# corredores
	if (x >= -15.6 and x <= 3.6) and (y >= -3.1 and y <= -1.4):
		return 1
	elif (x >= -11.8 and x <= -9.6) and (y > -1.4 and y < 5.5):
		return 2
	elif (x >= -11.8 and x <= 3.6) and (y >= 5.5 and y <= 7.3):
		return 3
	elif (x >= -4.0 and x <= -1.4) and (y > -1.4 and y < 5.5):
		return 4
	# quartos
	elif (x >= -15.6 and x <= -12.4) and (y >= -0.9 and y <= 2.3):
		return 5
	elif (x >= -15.6 and x <= -12.4) and (y >= 2.9 and y <= 7.3):
		return 6
	elif (x >= -15.6 and x <= -11.2) and (y >= 7.9 and y <= 11.0):
		return 7
	elif (x >= -10.2 and x <= -6.2) and (y >= 7.9 and y <= 11.0):
		return 8
	elif (x >= -5.6 and x <= -1.2) and (y >= 7.9 and y <= 11.0):
		return 9
	elif (x >= -0.6 and x <= 3.6) and (y >= 7.9 and y <= 11.0):
		return 10
	elif (x >= -0.9 and x <= 3.6) and (y >= 2.3 and y <= 4.8):
		return 11
	elif (x >= -0.9 and x <= 3.6) and (y >= -0.9 and y <= 1.7):
		return 12
	elif (x >= -9 and x <= -7.1) and (y >= -0.9 and y <= 4.8):
		return 13
	elif (x >= -6.5 and x <= -4.5) and (y >= -0.9 and y <= 4.8):
		return 14
	else:
		return 0

def checkObject(obj_set): # function that checks if each object "seen" by the agent is already in the sub-list of the list "Rooms" corresponding to the corrent_room
 	global current_room
 	for i in range(len(obj_set)):
 		if obj_set[i] in Rooms[current_room - 1]:
 			return True
 	return False

def checkSuite(room1, room2): # function that checks if a pair of rooms make a suite and adds them to the "Suites" list
	global Suites
	suite_set = [room1, room2]
	if room1 != 1 and room1 != 2 and room1 != 3 and room1 != 4 and room2 != 1 and room2 != 2 and room2 != 3 and room2 != 4:
		if not (suite_set in Suites or suite_set.reverse() in Suites):
			Suites.append(suite_set)

def countEmtpyRooms(): # function that checks which rooms, that have already been visited, don't have people present in them
	global Rooms
	count = 0
	substring = "person"
	for i in range(4, len(Rooms)):
		if not (Rooms[i][0] == "0"):
			if any(substring in full_string for full_string in Rooms[i]):
				continue
			count = count + 1
	return count

def getRoomType(room_num): # function return the room type given the room number
	global Rooms, Suites
	bed = "bed"
	bed_count = 0
	table = "table"
	table_count = 0
	chair = "chair"
	chair_count = 0
	if room_num < 4:
		return "corridor"
	bed_count = sum(bed in fullstring for fullstring in Rooms[room_num])
	table_count = sum(table in fullstring for fullstring in Rooms[room_num])
	chair_count = sum(chair in fullstring for fullstring in Rooms[room_num])
	if any(room_num in sublist for sublist in Suites):
		return "suite"
	if bed_count == 0:
		if table_count == 1:
			if chair_count > 1:
				return "meeting room"
			return "generic room"
		return "generic room"
	elif bed_count == 1:
		center_x, center_y = getRoomCenter(room_num)
		if any(room_num in sublist for sublist in Single_rooms):

			Single_rooms.append([room_num, center_x, center_y])
		return "single room"
	elif bed_count == 2:
		return "double room"


def answerCentral(question): # function that handles the answering process of each question 
	num = int(question[0])
	if num == 1:
		count1 = countEmtpyRooms()
		if count1 == 1:
			print("The agent has found one that is not occupied")
		else:
			print("The agent has found " + str(num) + " rooms that are not occupied")
	#----------------------------------------------------------------------------------------------
	elif num == 2:
		global Suites
		count2 = len(Suites)
		if count2 == 1:
			print("The agent has found one suite so far")
		else:
			print("The agent has found " + str(num) + " suites so far")
	#----------------------------------------------------------------------------------------------
	elif num == 3:
		global Rooms
		countR = 0 # count Rooms
		countH = 0 # count Halls
		substring = "person"
		for i in range(0, len(Rooms)):
	 		if i < 4: # for the corridors
	 			if not(Rooms[i][0] == "0"): # check to see if a room has been visited yet // rooms that have not been visited have the first string of the sublist at "0"
 					countH = countH + sum(substring in fullstring for fullstring in Rooms[i])# add up all the people in the hall #i to the total of people in the halls
	 		else: # for the rooms
	 			if not(Rooms[i][0] == "0"): 
	 				countR = countR + sum(substring in fullstring for fullstring in Rooms[i])# add up all the people in the room #i to the total of people in the rooms
		if countR > countH:
			print("It is more probable to find people in rooms rather than in the corridors")
		elif countR == countH:
			print("It is equally likely to find people in both the rooms and the corridors")
		else:
			print("It is more likely to find people in the corridors than in the rooms")
	#----------------------------------------------------------------------------------------------
	elif num == 4:
		global Rooms
		computer = "computer"
		count4 = True
		for i in range(0, len(Rooms)):
			if any(computer in fullstring for fullstring in Rooms[i]): # check to see if there are any computers in the list of objects found in room i
				print("To find a computer, the agent should head to a " + Rooms[i][1])
				count4 = False # if a computer is found this variable is set to false as to not trigger the complementary answer below
				break
		if count4:
			print("No computers have been found so far")
	#----------------------------------------------------------------------------------------------
	elif num == 5:
		global Single_rooms
		roomlist = []
		for i in range(len(Single_rooms)):
			roomlist.append([i, math.sqrt((Single_rooms[i][1] - current_position[0])**2 + (Single_rooms[i][2] - current_position[1])**2)]) # add to the local list of rooms the number and distance of every known single room
		roomlist = sorted(roomlist, key=itemgetter(1)) # sort the local room list by the distance
		print(" The closest single room is " + str(roomlist[0][0])) # print the number of the first element in the list, which is the one with the lowest distance value
	#----------------------------------------------------------------------------------------------
	elif num == 6:
		# TODO: generate a graph using the current_room and previous_room variables to create the vectors
		#       apply Dijkstra between the node with the current room and node 1 (which holds the only connection to the elevator)
		print("Not Implemented")
	#----------------------------------------------------------------------------------------------
	elif num == 7:
		# TODO: create a new list to write the time everytime a new book is found
		#       create an estimate to the amount of books that can be found with the next 2 minutes
		print("Not Implemented")
	#----------------------------------------------------------------------------------------------
	elif num == 8:
		countTables = 0.0
		countRooms = 0.0
		for i in range(len(Rooms)):
			if any("chair" in substring for substring in Rooms[i]):
				if any("book" in secondsubstring for secondsubstring in Rooms[i]):
					continue
				else:
					if any("table" in thirdsubstring for thirdsubstring in Rooms[i]):
						countTables = countTables + 1.0
					countRooms = countRooms + 1.0
		if countRooms == 0:
			print("Ainda não foi observado nenhum quarto que corresponde ao tipo descrito.")
		else:
			print("A probabilidade é de " + str(countTables/countRooms))
	
# ----------------Default functions------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, current_position, current_room, Rooms
	check = 0
	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print("x=%.1f y=%.1f" % (x,y))
		# new code----------------------
		current_position = [x, y]
		if room_coordinates(x, y) != current_room and room_coordinates(x, y) != 0: # check if the agent has changed rooms
			previous_room = current_room
			current_room = room_coordinates(x, y)
			checkSuite(previous_room, current_room)
			if Rooms[current_room - 1][0] == "0": # update global list "Rooms" with the number of the current room if this is the first time visiting it
				Rooms[current_room - 1].insert(0, str(current_room))
				Rooms[current_room - 1].remove("0")
		#-------------------------------
	x_ant = x
	y_ant = y
# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant, Rooms, current_room
	obj = data.data
	if obj != obj_ant and data.data != "":
		print("object is %s" % data.data)
		# new code----------------------
		obj_set = obj.split(",") # separate the objects into a list in case the agent spots multiple objects at once
		if not checkObject(obj_set): # check to see if the objects are being seen for the first time
		  	for i in range(len(obj_set)): 
		  		Rooms[current_room - 1].append(obj_set[i]) # add the objects to the global list "Rooms" in their room's corresponding sublist
			Rooms[current_room - 1].insert(1, getRoomType(current_room - 1)) # get and add the room type to the global list "Rooms" in their room's corresponding sublist
			del Rooms[current_room - 1][2] # remove the previous room_type assigned
		#-------------------------------
	obj_ant = obj
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print("question is %s" % data.data)
	answerCentral(data.data)
	
# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')
    
	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()
 # ---------------------------------------------------------------
if __name__ == '__main__':
	agent()