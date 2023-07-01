import socket
import pickle
import pygame
from player import *
from FCommands import *
import threading
import concurrent.futures
import sys
import time
from Platform import *
from FrecvDataFactory import RecvDataFactory
from Pickup import *
from Background import Background
from LifeBar import LifeBar
from ObjectInGame import *
from Bullet import *
from Gravita import Gravita
from TrigerredZone import *


background = Background("supreme")
lista_platforms = list()
lista_pickups = list()
lista_bullet = list()
lista_trigerred = list()
lista_ghosts_platforms = list()


print("ALL FILES IS LOAD")
PING = float(input("PING -> "))

f = open(f"packets_{PING}.txt" , "w")


z = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_udp_informations = ('2.85.254.22',20000)

counter_server = 0

lista_players = list()

def send_udp(data,address):
	try:
		time.sleep(PING)
		z.sendto(pickle.dumps(data),address)
	except:
		return None

def recv_udp(buffer_size = 5120):
	try:
		time.sleep(PING)
		return pickle.loads(z.recvfrom(buffer_size)[0])
	except:
		return None


counter = 0
lista_queue = list()


def recv_and_update():
	global lista_players
	global lista_platforms
	global lista_pickups
	global lista_bullet
	global lista_trigerred
	global lista_ghosts_platforms
	global counter_server
	global no_key
	global counter
	start = time.time()
	send_udp((Recv(),None),server_udp_informations)
	last_server = counter_server
	recv_data , counter_server = recv_udp()
	#print(f"PING -> {(time.time() - start) * 100}")
	if recv_data != None:
		#print(f"Buffer Size -> {len(pickle.dumps(recv_data))}")
		lista_players_new = RecvDataFactory.getRecvData(recv_data,Player,lista_players)
		print(counter_server,counter)
		f.write(f"{counter_server} - {counter} \n")
		if counter_server >= last_server:
			for i in range(counter_server,counter):
				if isinstance(lista_queue[i][0],Key_D):
					#print("Key D Prediction")
					if not lista_players_new[ID_PLAYER].AnimStart:
						lista_players_new[ID_PLAYER].setStatus(0)
						lista_players_new[ID_PLAYER].setSide(1)
						lista_players_new[ID_PLAYER].move_collide([20,0],[platform.getHitBox() for platform in lista_platforms])
				if isinstance(lista_queue[i][0],Key_A):
					#print("Key A Prediction")
					if not lista_players_new[ID_PLAYER].AnimStart:
						lista_players_new[ID_PLAYER].setStatus(0)
						lista_players_new[ID_PLAYER].setSide(0)
						lista_players_new[ID_PLAYER].move_collide([-20,0],[platform.getHitBox() for platform in lista_platforms])
				if isinstance(lista_queue[i][0],Key_SPACE):
					lista_players_new[ID_PLAYER].move_collide([0,-220],[platform.getHitBox() for platform in lista_platforms])
					lista_players_new[ID_PLAYER].isJump = True
				if isinstance(lista_queue[i][0],Key_W):
					lista_players_new[ID_PLAYER].move_collide([0,-10],[platform.getHitBox() for platform in lista_platforms])
				if isinstance(lista_queue[i][0],Key_S):
					lista_players_new[ID_PLAYER].move_collide([0,10],[platform.getHitBox() for platform in lista_platforms])
				if isinstance(lista_queue[i][0],Key_V):
					lista_players_new[ID_PLAYER].skin_counter = 0
					lista_players_new[ID_PLAYER].setStatus(4)
					lista_players_new[ID_PLAYER].AnimStart = True
				if isinstance(lista_queue[i][0],No_Key):
					if not lista_players_new[ID_PLAYER].AnimStart and lista_players_new[ID_PLAYER].getHealth() > 0:
						lista_players_new[ID_PLAYER].setStatus(2)
				if lista_queue[i][0] == Gravita:
					#print("ON GRAVITA")
					Gravita.apply(lista_players_new[ID_PLAYER],lista_platforms)
					lista_players_new[ID_PLAYER].setJump([platform.getHitBox() for platform in lista_platforms])


			lista_players = list(lista_players_new)

		
		#lista_players = RecvDataFactory.getRecvData(recv_data,Player,lista_players)

		lista_platforms = RecvDataFactory.getRecvData(recv_data,Platform,lista_platforms)
		lista_pickups = RecvDataFactory.getRecvData(recv_data,Pickup,lista_pickups)
		lista_bullet = RecvDataFactory.getRecvData(recv_data,Bullet,lista_bullet)
		lista_trigerred = RecvDataFactory.getRecvData(recv_data,TrigerredZone,lista_trigerred)
		lista_ghosts_platforms = RecvDataFactory.getRecvData(recv_data,GhostPlatform,lista_ghosts_platforms)

send_udp(("JOIN",TonyEffe),server_udp_informations)

ID_PLAYER = int(recv_udp())
print(ID_PLAYER)

send_udp((Recv(),None),server_udp_informations)
recv_and_update()

lista_queue = list()


pygame.init()
win = pygame.display.set_mode((1360, 768))
run = True

ObjectInGame.win = win
"""
progress_bars = [LifeBar(150,50,lista_players[0].name,lista_players[0].face,100),
				LifeBar(1150,50,lista_players[1].name,lista_players[1].face,100)]
"""
clock = pygame.time.Clock()

while  run:
	z.settimeout(6)
	no_key = True
	clock.tick(120)
	#UPDATE ALL THE STATE OF THE GAME  

	#with concurrent.futures.ThreadPoolExecutor() as executor:
	#	future = executor.submit(recv_udp)

	threading.Thread(target= recv_and_update).start()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			f.close()

	keys = pygame.key.get_pressed()

	win.fill((255,200,20))

	background.spawn(win)

	try: 
		for player in lista_players:
			player.spawn(win)
	except Exception as e:
		print(e)

	for platform in lista_platforms:
		platform.spawn(win)

	for pickup in lista_pickups:
		pickup.spawn(win)

	for bullet in lista_bullet:
		bullet.spawn()
	
	for trigerred in lista_trigerred:
		trigerred.spawn(win)

	for ghost in lista_ghosts_platforms:
		ghost.spawn(win)
	"""
	for ID in range(2):
		for ID_ in range(2):
			if lista_players[ID].collide(progress_bars[ID_].hitBox):
				progress_bars[ID_].move([0,-30])
			elif not lista_players[ID].collide(progress_bars[ID_].hitBox) and progress_bars[ID_].y <= 50:
				progress_bars[ID_].move([0,1])

	for ID in range(2): 
		progress_bars[ID].setBullets(lista_players[ID].weapon.getAmmo())
		progress_bars[ID].setLife(lista_players[ID].getHealth())
		progress_bars[ID].spawn() #OBJECT IN GAME
	"""

	if keys[pygame.K_d] and not lista_players[ID_PLAYER].AnimStart:
		counter += 1
		lista_queue.append((Key_D(),counter))
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_D(),counter),server_udp_informations,))
		send_commands_thread.start()
		if not lista_players[ID_PLAYER].AnimStart:
			if lista_players[ID_PLAYER].status != 0:
				lista_players[ID_PLAYER].skin_counter = 0
			lista_players[ID_PLAYER].setStatus(0)
			lista_players[ID_PLAYER].setSide(1)
			lista_players[ID_PLAYER].move_collide([20,0],[platform.getHitBox() for platform in lista_platforms])

	if keys[pygame.K_a] and not lista_players[ID_PLAYER].AnimStart:
		lista_queue.append((Key_A(),counter))
		counter += 1
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_A(),counter),server_udp_informations,))
		send_commands_thread.start()
		if not lista_players[ID_PLAYER].AnimStart:
			if lista_players[ID_PLAYER].status != 0:
				lista_players[ID_PLAYER].skin_counter = 0
			lista_players[ID_PLAYER].setStatus(0)
			lista_players[ID_PLAYER].setSide(0)
			lista_players[ID_PLAYER].move_collide([-20,0],[platform.getHitBox() for platform in lista_platforms])

	if keys[pygame.K_w]:
		lista_queue.append((Key_W(),counter))
		counter += 1
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_W(),counter),server_udp_informations,))
		send_commands_thread.start()
		lista_players[ID_PLAYER].move_collide([0,-10],[platform.getHitBox() for platform in lista_platforms])

	if keys[pygame.K_s]:
		lista_queue.append((Key_S(),counter))
		counter += 1
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_S(),counter),server_udp_informations,))
		send_commands_thread.start()
		lista_players[ID_PLAYER].move_collide([0,10],[platform.getHitBox() for platform in lista_platforms])

	if keys[pygame.K_v]:
		lista_queue.append((Key_V(),counter))
		counter += 1
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_V(),counter),server_udp_informations,))
		send_commands_thread.start()
		lista_players[ID_PLAYER].skin_counter = 0
		lista_players[ID_PLAYER].setStatus(4)
		lista_players[ID_PLAYER].AnimStart = True

	if keys[pygame.K_e]:
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_E(),counter),server_udp_informations,))
		send_commands_thread.start()
	
	if keys[pygame.K_l]:
		#counter += 1
		#lista_queue.append((Key_L(),counter))
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_L(),counter),server_udp_informations,))
		send_commands_thread.start()

	if keys[pygame.K_SPACE] and not lista_players[ID_PLAYER].AnimStart and not lista_players[ID_PLAYER].isJump:
		lista_queue.append((Key_SPACE(),counter))
		counter += 1
		no_key = False
		send_commands_thread = threading.Thread(target = send_udp , args=((Key_SPACE(),counter),server_udp_informations,))
		send_commands_thread.start()
		lista_players[ID_PLAYER].move_collide([0,-220],[platform.getHitBox() for platform in lista_platforms])
		lista_players[ID_PLAYER].isJump = True

	if no_key:
		lista_queue.append((No_Key(),counter))
		counter += 1
		send_commands_thread = threading.Thread(target = send_udp , args=((No_Key(),counter),server_udp_informations,))
		send_commands_thread.start()
		if not lista_players[ID_PLAYER].AnimStart and lista_players[ID_PLAYER].getHealth() > 0:
			lista_players[ID_PLAYER].setStatus(2)

	lista_players[ID_PLAYER].playAnimation()
	
	Gravita.apply(lista_players[ID_PLAYER],lista_platforms)
	lista_players[ID_PLAYER].setJump([platform.getHitBox() for platform in lista_platforms])
	counter += 1
	lista_queue.append((Gravita,counter))




	"""

	recv_data = future.result()
	if recv_data != None:
		print(f"Buffer Size -> {len(pickle.dumps(recv_data))}")
		lista_players = RecvDataFactory.getRecvData(recv_data,Player,lista_players)
		lista_platforms = RecvDataFactory.getRecvData(recv_data,Platform,lista_platforms)
		lista_pickups = RecvDataFactory.getRecvData(recv_data,Pickup,lista_pickups)
		lista_bullet = RecvDataFactory.getRecvData(recv_data,Bullet,lista_bullet)
	"""

	pygame.display.update()