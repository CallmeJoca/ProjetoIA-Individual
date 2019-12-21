#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Jorge Pissarra, a39489

# TODO: 
# - fazer metodo set para o tipo de quarto quando se entra num quarto
# - fazer metodo atualização dos objetos contidos num quarto
# - fazer metodo atualização das pessoas a ocupar cada quarto
# - fazer metodo atualização do atual quarto onde se encontra o agente
# - fazer função de geração das coordenadas de cada quarto para inicializar o array de objetos tipo QUARTO
# - fazer print com chamada para a função que devolve a resposta à pergunta selecionada pelo utilizador
# - 

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

count_Suites_visited = 0
prev_room_visisted = 0
room_current = 1
x_ant = 0
y_ant = 0
obj_ant = ''
Agente = Agent([0,0], 1, -1, [1])

def coordinates_list():
    return [(1,2),(3,4)] # replace with coordinates 

#-----------------Start of Room Class----------------------------
class Room:
    def __init__(self, starting_number, starting_coordinates, starting_room_type, starting_occupancy, starting_objects):
        self.number = starting_number
        self.coordinates = starting_coordinates
        self.room_type = starting_room_type
        self.occupancy = starting_occupancy
        self.objects = starting_objects

    def get_number(self):
		return self.number

    def get_coordinates(self):
        return self.coordinates

    def get_room_type(self):
        return self.room_type

    def set_room_type(self):
        count_beds = 0
        count_tables = 0
        count_chairs = 0
        for i in self.objects:
            if self.objects[i] == "bed":
                count_beds = count_beds + 1
            if self.objects[i] == "table":
                count_tables = count_tables + 1
            if self.objects[i] == "chair":
                count_chairs = count_chairs + 1
        if count_beds == 0:
            if count_tables == 1:
                if count_chairs > 1:
                    self.room_type = "Meeting Room"
        elif count_beds == 1:
            self.room_type = "Single"
        elif count_beds == 2:
            self.room_type = "Double"
        else:
            self.room_type = "Generic"
        
    def get_occupancy(self):
        return self.occupancy
    
    def set_occupancy(self, new_occupancy):
        self.occupancy.append(new_occupancy)
    
    def get_objects(self):
        return self.objects
    
    def set_objects(self, new_object):
        self.objects.append(new_object)
    
    def Check_Objects(self, object_found):
        for i in self.objects:
            if self.objects[i] == object_found:
                return True
        return False
    

# -----------------End of Room Class-----------------------------

# ----------------Start of Agent Class---------------------------
class Agent:
    def __init__(self, starting_position, starting_current_room, starting_previous_room, starting_Rooms_Visited):
        self.position = starting_position
        self.current_room = starting_current_room
        self.previous_room = starting_previous_room
        self.Rooms_Visited = starting_Rooms_Visited

    def get_position(self):
        return self.position
    
    def set_position(self, new_position):
        self.position = new_position

    def get_current_room(self):
        return self.current_room

    def set_current_room(self, new_current_room):
        self.current_room = new_current_room

    def get_previous_room(self):
        return self.previous_room

    def set_previous_room(self, new_previous_room):
        self.previous_room = new_previous_room
    
    def get_Rooms_Visited(self):
        return self.Rooms_Visited
    
    def set_Rooms_Visited(self, new_Rooms_Visited):
        self.Rooms_Visited = new_Rooms_Visited

    def Number_Free_Rooms(self, Quarto):
        counter = 0
        for i in self.get_Rooms_Visited:
            if len(Quarto[i].get_occupancy) != 0:
                counter = counter + 1
        return counter

    def Number_Suites_Found(self, Quarto):
        counter = 0
        for i in self.get_Rooms_Visited:
            if Quarto[i].get_room_type == "Suite":
                counter = counter + 1
        return counter

    def Probability_People_In_Rooms(self, Quarto):
        number_people_halls = 0
        number_people_rooms = 0
        for i in self.get_Rooms_Visited:
            if Quarto[i].get_room_type == "Hall":
                number_people_halls = number_people_halls + Quarto[i].get_occupancy
            else:
                number_people_rooms = number_people_rooms + Quarto[i].get_occupancy
        if number_people_halls > number_people_rooms:
            return -1
        elif number_people_halls < number_people_rooms:
            return 1
        else:
            return 0

    def Check_If_Suite(self):
        if self.get_previous_room > 4:
            return True
        return False 

# ------------------End of Agent Class---------------------------

# -----------------Start of Object Class ------------------------

class Object:
    def __init__(self, starting_tipo, starting_name, starting_room):
        self.tipo = starting_tipo
        self.name = starting_name
        self.room = starting_room

    def get_tipo(self):
        return self.type
    def set_tipo(self, new_tipo):
        self.tipo = new_tipo
    def get_name(self):
        return self.name
    def set_name(self, new_name):
        self.name = new_name
    def get_room(self):
        return self.room
    def set_room(self, new_room):
        self.room = new_room

# ------------------End of Object Class--------------------------

# Criar um array de instancias da classe Room para representar 
# os 4 corredores e os 10 quartos
def Define_Rooms(coordinates):
    
    for i in range(14):
        if i < 5:
            Quarto[i] = Room(i+1, coordinates[i], "Corredor", 0, [])
        Quarto[i] = Room(i+1, coordinates[i], "Quarto", 0, [])

# ----------------Default functions------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print("x=%.1f y=%.1f" % (x,y))
        Agent.set_position(Agent, [x,y])
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant and data.data != "":
		print("object is %s" % data.data)
        
	obj_ant = obj

# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print("question is %s" % data.data)

# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')

	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()

 # ---------------------------------------------------------------
if __name__ == '__main__':

    Define_Rooms(coordinates_list)
	
    agent()