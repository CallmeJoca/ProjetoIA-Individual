#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2016
# Modified by:
#	Nelson Fonseca, 33514
#	Vasco Lopes,    34507

import networkx as nx
import math
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''
lista=[]
lista_no_rep=[]
room_ant = 1

listOfLists = [] #vai ter 12 listas, 1 para cada room
for i in xrange(0,12):
	listOfLists.append([]) #vai da lista 0 a lista 11

G = nx.Graph()
G.add_node(1);
# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant, room_ant
	x=data.pose.pose.position.x
	y=data.pose.pose.position.y
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		if hasRoomChanged(x,y,room_ant):
			G.add_edge(room_ant,getRoom(x,y))
		print (" x=%.1f y=%.1f" % (x,y))
	x_ant = x
	y_ant = y
	room_ant = getRoom(x,y)

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant:
		print ("object is %s" % data.data)
		if data.data != "":
			listasplited = data.data.split(',')
			roomActual = getRoom(x_ant,y_ant)
			for x in xrange(0,len(listasplited)):
				if listasplited[x] not in listOfLists[roomActual-1]: #vai de 0 a 11 e as salas sao de 1 a 12					
					listOfLists[roomActual-1].append(listasplited[x])

				if listasplited[x] not in lista_no_rep:
					lista_no_rep.append(listasplited[x])

				lista.append((listasplited[x],x_ant,y_ant))

			
	obj_ant = obj
# ---------------------------------------------------------------
def hasRoomChanged(x,y,ant):
	actual = getRoom(x,y)
	if ant == actual:
		return False
	return True
# ---------------------------------------------------------------
def getRoom(x,y): #para não ser X_ANT e Y_ANT, conveniencia
	if (x<=4.0 and x>=-1.0)   and   (y>=-3.5 and y<=1.5):
		return 1
	if (x<-1.0 and x>=-6.0)   and   (y>=-3.5 and y<=1.5): 
		return 2
	if (x<-6.0 and x>=-11.0)  and   (y>=-3.5 and y<=1.5):
		return 3	
	if (x<-11.0 and x>=-16.0) and   (y>=-3.5 and y<=1.5): 
		return 4	
	if (x<=4.0 and x>=-1.0)   and   (y>1.5 and y<=6.5): 	
		return 5
	if (x<-1.0 and x>=-6.0)   and   (y>1.5 and y<=6.5): 
		return 6	
	if (x<-6.0 and x>=-11.0)  and   (y>1.5 and y<=6.5): 
		return 7	
	if (x<-11.0 and x>=-16.0) and   (y>1.5 and y<=6.5): 
		return 8	
	if (x<=4.0 and x>=-1.0)   and   (y>6.5 and y<=11.5): 	
		return 9
	if (x<-1.0 and x>=-6.0)   and   (y>6.5 and y<=11.5): 
		return 10
	if (x<-6.0 and x>=-11.0)  and   (y>6.5 and y<=11.5): 	
		return 11
	if (x<-11.0 and x>=-16.0) and   (y>6.5 and y<=11.5): 	
		return 12	
#----------------------------------------------------------------
def roomType(currRoom): #currRoom é a sala
	chairs = 0
	tables = 0
	books = 0
	computers = 0
	persons = 0
	flag = 0

	if (len(listOfLists[currRoom-1])) != 0:
		for x in xrange(0, len(listOfLists[currRoom-1])):
			listasplited = listOfLists[currRoom-1][x].split('_')

			if listasplited[0] == "person":
				persons = persons +1
			if listasplited[0] == "book":
				books = books +1
			if listasplited[0] == "computer":
				computers = computers +1
			if listasplited[0] == "table":
				tables = tables +1
			if listasplited[0] == "chair":
				chairs = chairs +1

	if tables == 0 and books == 0 and computers == 0 and persons == 0 and chairs != 0:
		return "waiting room"
		flag = 1
	elif chairs != 0 and tables != 0 and books != 0 and computers == 0:
		return "study room"
		flag = 1
	elif computers != 0 and tables != 0 and chairs != 0:
		return "computer lab"
		flag = 1
	elif tables == 1 and chairs >= 2: #significa que meeting room tem de ter 1 mesa e 2 ou mais cadeiras
		return "meeting room"
		flag = 1
	
	if flag == 0:
		return "generic room"
#----------------------------------------------------------------
#pergunta A
def pa():
	if len(lista) > 0:
		(a,b,c) = lista[-1]
		print (a)
	else:
		print ("Insufficient information")
#----------------------------------------------------------------
#pergunta B
def pb():
	print (len(lista_no_rep))
# ---------------------------------------------------------------
#pergunta C
def pc():
	disteucl = 0
	minDistEucl = 999
	objectCloser = "Insufficient information"

	for x in xrange(0,len(lista)):
		(a,b,c) = lista[x]
		disteucl = math.sqrt( ((x_ant - b) * (x_ant - b)) + ((y_ant - c) * (y_ant - c)) ) #calcula a distancia eucladiana
		if disteucl < minDistEucl:
			minDistEucl = disteucl
			objectCloser = a
	
	print (objectCloser)
# ---------------------------------------------------------------
#pergunta D
def pd():
	x_joe = -10
	y_joe = -10
	minDistEucl = 999
	objectCloser = "I haven't seen Joe yet"

	for x in xrange(0,len(lista)):
		(a,b,c) = lista[x]
		if a == "person_joe":
			x_joe = b
			y_joe = c
			break
	
	if x_joe != -10 and y_joe != -10:
		for x in xrange(0,len(lista)):
			(a,b,c) = lista[x]
			if a == "person_joe":
				continue
			distEucl = math.sqrt( ((x_joe - b) * (x_joe - b)) + ((y_joe - c) * (y_joe - c)) )
			if distEucl < minDistEucl:
				minDistEucl = distEucl
				objectCloser = a
	
	print (objectCloser)
# ---------------------------------------------------------------
#pergunta E
def pe():
	count = 0

	for x in xrange (0,len(lista_no_rep)):
		a = lista_no_rep[x]
		listasplited = a.split('_')

		if listasplited[0] == 'book':		
			count = count + 1
	
	print (count)
# ---------------------------------------------------------------
#pergunta F
def pf():
	resposta = "I haven't seen Mary yet"		

	for x in xrange (0,len(lista_no_rep)):
		if lista_no_rep[x] == "person_mary":
			resposta = "I've seen Mary"
			break	
	print (resposta)
# ---------------------------------------------------------------
#pergunta G
def pg():
	resposta = "I haven't seen Joe yet"

	for x in xrange(0, len(lista)):
		(a,b,c) = lista[x]
		if a == "person_joe":
			resposta = "Joe is at Room " + str(getRoom(b,c))
			break
	
	print (resposta)

# ---------------------------------------------------------------
#pergunta H
def ph():
	flag = 0

	for i in xrange(0,12):
		if flag == 1:
			break

		for j in xrange (0, len(listOfLists[i])): #acede a lista i dentro da lista de listas
			listasplited = listOfLists[i][j].split('_')			

			if listasplited[0] == 'table':
				flag = 1
				break

	if flag == 1:
		print ("Yes, there are")
	else:
		print ("I haven't seen any room with tables yet")
# ---------------------------------------------------------------
#pergunta I
def pi():
	listNodesVisited = G.nodes()
	x = "Rooms visited: "	
	
	for i in xrange(0, len(listNodesVisited)): 	#transformar a lista em string
		x = x + str(listNodesVisited[i]) + " "

	print (x)	#imprimir uma menasgem bonita
# ---------------------------------------------------------------
#rede bayesiana
def f_CHAIR( chair):
	roomWithChair = 0
	roomWithoutChair = len(G.nodes())

	for i in xrange(0,len(listOfLists)):
			for j in xrange(0,len(listOfLists[i])):
				a = listOfLists[i][j]
				listasplited = a.split('_')
				if listasplited[0] == "chair":
					roomWithChair = roomWithChair +1
					roomWithoutChair = roomWithoutChair-1
					break
 
	if chair == True: #c false
		if(roomWithoutChair == 0 and roomWithChair == 0):
			return 0
		return (float(roomWithChair) / (float(roomWithoutChair)+float(roomWithChair)))
	else: #c true
		if(roomWithoutChair == 0 and roomWithChair == 0):
			return 0
		return (1-(float(roomWithChair) / (float(roomWithoutChair)+float(roomWithChair))))

def f_TABLE(table, chair):
	roomChairTable = 0
	roomNoChairTable = len(G.nodes())
	
	flagChair = 0
	flagTable = 0	

	if table == True: #t true
		if chair == True: #t, c true
			for i in xrange(0,len(listOfLists)):
				flagChair = 0
				flagTable = 0
				for j in xrange(0,len(listOfLists[i])):
					a = listOfLists[i][j]
					listasplited = a.split('_')
					if listasplited[0] == "chair":
						flagChair = 1
					if listasplited[0] == "table":
						flagTable = 1
				
				if(flagChair == 1 and flagTable == 1):
					roomChairTable = roomChairTable +1
					roomNoChairTable = roomNoChairTable -1

			if(roomChairTable == 0 and roomNoChairTable == 0):
				return 0
			return (float(roomChairTable) / (float(roomNoChairTable)+float(roomChairTable)))

		else: #t true | c false
			for i in xrange(0,len(listOfLists)):
				flagChair = 0
				flagTable = 0
				for j in xrange(0,len(listOfLists[i])):
					a = listOfLists[i][j]
					listasplited = a.split('_')
					if listasplited[0] == "chair":
						flagChair = 1
					if listasplited[0] == "table":
						flagTable = 1
				
				if(flagChair != 1 and flagTable == 1):
					roomChairTable = roomChairTable +1
					roomNoChairTable = roomNoChairTable -1

			if(roomChairTable == 0 and roomNoChairTable == 0):
				return 0
			return (float(roomChairTable) / (float(roomNoChairTable)+float(roomChairTable)))

	else: #t false
		if chair == True: #t false | c true
			for i in xrange(0,len(listOfLists)):
				flagChair = 0
				flagTable = 0
				for j in xrange(0,len(listOfLists[i])):
					a = listOfLists[i][j]
					listasplited = a.split('_')
					if listasplited[0] == "chair":
						flagChair = 1
					if listasplited[0] == "table":
						flagTable = 1
				
				if(flagChair == 1 and flagTable != 1):
					roomChairTable = roomChairTable +1
					roomNoChairTable = roomNoChairTable -1
	
			if(roomChairTable == 0 and roomNoChairTable == 0):
				return 0
			return (float(roomChairTable) / (float(roomNoChairTable)+float(roomChairTable)))

		else: #t false | c false
			for i in xrange(0,len(listOfLists)):
				flagChair = 0
				flagTable = 0
				for j in xrange(0,len(listOfLists[i])):
					a = listOfLists[i][j]
					listasplited = a.split('_')
					if listasplited[0] == "chair":
						flagChair = 1
					if listasplited[0] == "table":
						flagTable = 1
				
				if(flagChair != 1 and flagTable != 1):
					roomChairTable = roomChairTable +1
					roomNoChairTable = roomNoChairTable -1
	
			if(roomChairTable == 0 and roomNoChairTable == 0):
				return 0
			return (float(roomChairTable) / (float(roomNoChairTable)+float(roomChairTable)))

def f_PERSON(table, chair, person):
	roomPersonChairTable=0
	roomNoPersonNoChairTable=len(G.nodes())

	flagChair = 0
	flagTable = 0
	flagPerson = 0

	if person == True:
		if table == True:
			if chair == True: #P,T,C TRUE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair == 1 and flagTable == 1 and flagPerson == 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1


				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable)))

			else: #P,T TRUE | C FALSE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair != 1 and flagTable == 1 and flagPerson == 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1				

				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable)))




		else: #table = false
			if chair == True: #P,C TRUE | T FALSE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair == 1 and flagTable != 1 and flagPerson == 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1
				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable)))

			else: # T,C FALSE | P TRUE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair != 1 and flagTable != 1 and flagPerson == 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1

				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable)))

	else: #P FALSE
		if table == True:
			if chair == True: #P FALSE | T,C TRUE

				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair == 1 and flagTable == 1 and flagPerson != 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1

				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable)))

			else: #P,C FALSE | T TRUE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair != 1 and flagTable == 1 and flagPerson != 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1

				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable))) 

		else: #T,P FALSE
			if chair == True: #P, T FALSE | C TRUE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair == 1 and flagTable != 1 and flagPerson != 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1

				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable))) 

			else: #P,T,C FALSE
				for i in xrange(0,len(listOfLists)):
					flagChair = 0
					flagTable = 0
					flagPerson = 0
					for j in xrange(0,len(listOfLists[i])):
						a = listOfLists[i][j]
						listasplited = a.split('_')
						if listasplited[0] == "chair":
							flagChair = 1
						if listasplited[0] == "table":
							flagTable = 1
						if listasplited[0] == "person":
							flagPerson = 1
				
					if(flagChair != 1 and flagTable != 1 and flagPerson != 1):
						roomPersonChairTable = roomPersonChairTable +1
						roomNoPersonNoChairTable = roomNoPersonNoChairTable -1

				if(roomPersonChairTable == 0 and roomNoPersonNoChairTable == 0):
					return 0.0
				return (float(roomPersonChairTable) / (float(roomPersonChairTable)+float(roomNoPersonNoChairTable))) 
# ---------------------------------------------------------------
#pergunta j
def pj():
	print ("The probability is: "+str((f_PERSON(False,True,True)*100))+"%")#table,chair,person
# ---------------------------------------------------------------
#pergunta K
def pk():
	flagPerson = 0
	flagTable  = 0
	roomPersonTable = 0
	roomNoPerson = 0

	for i in xrange(0,len(listOfLists)):
		flagPerson = 0
		flagTable  = 0
		for j in xrange(0,len(listOfLists[i])):
			a = listOfLists[i][j]
			listasplited = a.split('_')
			if listasplited[0] == "person":
				flagPerson = 1
			if listasplited[0] == "table":
				flagTable = 1
			if flagPerson == 1 and flagTable == 1:
				break
		if(flagPerson != 0 and flagTable != 0): #casos favoraveis (todas as salas com pessoas e mesas)
			roomPersonTable = roomPersonTable +1
		if(flagTable != 0): #casos possiveis (todas as salas com mesa!)
			roomNoPerson = roomNoPerson +1

	if(roomPersonTable == 0 and roomNoPerson == 0):
		print ("The probability is: "+str(0.0)+"%")
	else:
		varx = (float(roomPersonTable)/(float(roomNoPerson)))
		print ("The probability is: "+str(varx *100)+"%")
# ---------------------------------------------------------------
#pergunta L
def pl(x,y):
	currRoom = getRoom(x,y)
	chairs = 0
	tables = 0
	books = 0
	computers = 0
	persons = 0
	flag = 0

	if (len(listOfLists[currRoom-1])) != 0:
		for x in xrange(0, len(listOfLists[currRoom-1])):
			listasplited = listOfLists[currRoom-1][x].split('_')

			if listasplited[0] == "person":
				persons = persons +1
			if listasplited[0] == "book":
				books = books +1
			if listasplited[0] == "computer":
				computers = computers +1
			if listasplited[0] == "table":
				tables = tables +1
			if listasplited[0] == "chair":
				chairs = chairs +1

	if tables == 0 and books == 0 and computers == 0 and persons == 0 and chairs != 0:
		print ("Room " + str(currRoom) + " is a waiting room.")
		flag = 1
	elif chairs != 0 and tables != 0 and books != 0 and computers == 0:
		print ("Room " + str(currRoom) + " is a study room.")
		flag = 1
	elif computers != 0 and tables != 0 and chairs != 0:
		print ("Room " + str(currRoom) + " is a computer lab.")
		flag = 1
	elif tables == 1 and chairs >= 2: #significa que meeting room tem de ter 1 mesa e 2 ou mais cadeiras
		print ("Room " + str(currRoom) + " is a meeting room.")
		flag = 1
	
	if flag == 0:
		print ("Room " + str(currRoom) + " is a generic room.")
# ---------------------------------------------------------------
#pergunta M
def pm():
	listaFree = []
	flag = 0

	for i in xrange(1, 13):
		if i in G.nodes(): #para se o vertice ainda nao tiver sido reconhecido, nao o meter na lista final
			for j in xrange (0, len(listOfLists[i-1])):
				listasplited = listOfLists[i-1][j].split('_')
			
				if listasplited[0] == "person":
					flag = 1
					break
			if flag == 1:
				flag = 0
			else: #se no fim não tiver ocupado
				listaFree.append(i)
		else:
			continue;
	print (listaFree)

# ---------------------------------------------------------------
#Pergunta N
def pn():
	roomMary = -1

	flag = 0
	listComputers = []
	minDist = 999
	prefPc = ""
	x_mary = 0
	y_mary = 0
	#encontrar a mary
	for i in xrange(0, len(lista)):
		(a,b,c) = lista[i]
		if a == "person_mary":
			roomMary = getRoom(b,c)-1
			x_mary = b
			y_mary = c
			break

	if roomMary != -1:
		for t in xrange(0, len(listOfLists[roomMary])):
			listasplited = listOfLists[roomMary][t].split('_')

			if listasplited[0] == "computer":
				listComputers.append(listOfLists[roomMary][t])		
	
		if len(listComputers) == 0:
			print ("I haven't recognized any computer in the same room as Mary, so i can't say what computer Mary prefers.")
		elif len(listComputers) == 1:
			a = str(listComputers[0])
			if a[:16] == 'computer_windows':
				print ("I think Mary prefers Windows computers.")
			elif a[:14] == 'computer_apple':
				print ("I think Mary prefers Apple computers.")
			elif a[:16] == 'computer_windows' and a[:14] == 'computer_apple':
				print ("I think Mary prefers other brand...")
		elif len(listComputers) > 1:
			for w in xrange(0, len(listComputers)):
				for n in xrange(0, len(lista)): 
					if listcomputers[w] == lista[n]:
							(a,b,c) = lista[n]
							distEucl = math.sqrt( ((x_mary - b) * (x_mary - b)) + ((y_mary - c) * (y_mary - c)) )
							if distEucl < minDist:
								prefPc = a
								minDist = distEucl
							elif distEucl == minDist and (prefPc[:16] != 'computer_windows' or prefPc[:14] != 'computer_apple'):
								prefPc = a
								minDist = distEucl
								
			if prefPc[:16] == 'computer_windows':
				print ("I think Mary prefers Windows computers.")
			elif prefPc[:14] == 'computer_apple':
				print ("I think Mary prefers Apple computers.")
			elif prefPc[:16] == 'computer_windows' and prefPc[:14] == 'computer_apple':
				print ("I think Mary prefers other brand...")
	elif roomMary == -1:
		print ("I haven't seen Mary yet, so i can't say what computer Mary prefers.")

# ---------------------------------------------------------------
#Pergunta O
def po(x,y):
	listaCaminhos = []
	flag = 0
	if 9 in G.nodes():
		listaCaminhos = list(nx.all_simple_paths(G,getRoom(x,y),9)) #devolve todos os caminhos sem nodes repetidos em cada um.
		for i in xrange(0, len(listaCaminhos)):
			for j in xrange(0, len(listaCaminhos[i])):
				if listaCaminhos[i][j] == 7:
					break
				if j == len(listaCaminhos[i])-1:
					flag = 1			
		
			if flag == 1:
				print ("No, you don't.")
				break
		if flag == 0:
			print ("Yes, according to the representation of the world I have at the moment, you must pass at room 7 to reach room 9.")
	else:
		print ("I haven't recognized room 9 yet.")
# ---------------------------------------------------------------
#Pergunta P
def pp(x,y):
	listaCL = []
	roomActual = getRoom(x,y)
	maisCurto = []
	if roomType(roomActual) != "computer lab":
		aux = -1
		for x in xrange(1,13):
			if roomType(x) == "computer lab":
				if x == roomActual:
					continue			
				aux = x
				listaCL.append(x)

		if aux != -1:
			maisCurto = list(nx.dijkstra_path(G,roomActual,listaCL[0]))
			for i in xrange(1,len(listaCL)):
				caminhoMaisCurto = list(nx.dijkstra_path(G,roomActual,listaCL[i]))
				if (len(maisCurto) > len(caminhoMaisCurto)):
					maisCurto = caminhoMaisCurto
			print (maisCurto)
		else:
			print ("There are no recognized computer lab room yet.")
	else:
		print ("I'm already in a computer lab.")
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print ("question is %s" % data.data)
	if data.data == 'a':
		pa()
	if data.data == 'b':
		pb()
	if data.data == 'c':
		pc()
	if data.data == 'd':
		pd()
	if data.data == 'e':
		pe()
	if data.data == 'f':
		pf()
	if data.data == 'g':
		pg()
	if data.data == 'h':
		ph()
	if data.data == 'i':
		pi()
	if data.data == 'j':
		pj()
	if data.data == 'k':
		pk()
	if data.data == 'l':
		pl(x_ant,y_ant) #para os valores não mudaram enquanto executa
	if data.data == 'm':
		pm()
	if data.data == 'n':
		pn()
	if data.data == 'o':
		po(x_ant,y_ant)
	if data.data == 'p':
		pp(x_ant,y_ant)

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
