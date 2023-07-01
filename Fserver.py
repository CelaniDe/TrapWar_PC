import socket
import pickle
import pygame
from player import *
import threading
from FCommands import *
from Platform import *
import time
from Gravita import Gravita
from Pickup import *
from Bullet import *
from Map import Map
from playersSpawnPoints import *
from TrigerredZone import *

map_dict = Map.loadMap("lavanuova")

print(map_dict)

NUMEBR_OF_PLAYERS = 2

first_player_position = map_dict['Player'][0]

second_player_position = map_dict['Player'][1]

lista_players = [SferaEbbasta(first_player_position.x,first_player_position.y),
				SocialBoom(second_player_position.x,second_player_position.y)]

lista_platforms =  list(map_dict['Platform']) #[Brick(i,700) for i in range(-102,1360,102)]  

lista_pickups = list(map_dict['Pickup']) #[PurpleDrank(700,100),RayGun(500,200),Ammo(900,0)]
lista_pickups_respawn = list()

lista_bullet = list()

lista_trigerred = list(map_dict['Trigger']) #[TrigerredZone(600,200,200,200,ElevatorUse())]

lista_ghosts_platforms = list(map_dict['Ghosts'])

z = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
z.bind(("192.168.1.55",20000))


def send_udp(data,address):
	z.sendto(pickle.dumps(data),address)

d = dict()
while  len(d) < NUMEBR_OF_PLAYERS:
	data , address = z.recvfrom(1024)
	d[address] = len(d)
	print(f"Connected {address}")

lista_counters = [0,0]

for address in d:
	send_udp(d[address],address)
	time.sleep(0.3)
	send_udp(lista_players,address)
	time.sleep(0.3)
	send_udp(lista_platforms,address)
	time.sleep(0.3)
	send_udp(lista_pickups,address)
	time.sleep(0.3)
	send_udp(lista_bullet,address)
	time.sleep(0.3)
	send_udp(lista_trigerred,address)
	time.sleep(0.3)
	send_udp(lista_ghosts_platforms,address)

print("Sented")

def handling_request(data,address):
	data = pickle.loads(data)
	if type(data) == tuple:
		if data[0] == str and isinstance(data[1],Player):
			data , player_selected = data
		else:
			data , counter = data
	if isinstance(data,Commands):
		if counter != None:
			lista_counters[d[address]] = counter
		if isinstance(data,Key_D) and not lista_players[d[address]].AnimStart:
			lista_players[d[address]].setStatus(0)
			lista_players[d[address]].setSide(1)
			lista_players[d[address]].move_collide([20,0],[platform.getHitBox() for platform in lista_platforms])
			#print(f"{address} Press D")
		elif isinstance(data,Key_A) and not lista_players[d[address]].AnimStart:
			lista_players[d[address]].setStatus(0)
			lista_players[d[address]].setSide(0)
			lista_players[d[address]].move_collide([-20,0],[platform.getHitBox() for platform in lista_platforms])
			#print(f"{address} Press A")
		elif isinstance(data,Key_W):
			lista_players[d[address]].move_collide([0,-10],[platform.getHitBox() for platform in lista_platforms])
			#lista_platforms.remove(lista_platforms[-1])
		elif isinstance(data,Key_S):
			lista_players[d[address]].move_collide([0,10],[platform.getHitBox() for platform in lista_platforms])
		elif isinstance(data,Key_V)  and not lista_players[d[address]].AnimStart:
			lista_players[d[address]].skin_counter = 0
			lista_players[d[address]].setStatus(4)
			lista_players[d[address]].AnimStart = True
		elif isinstance(data,Key_L):
			if(lista_players[d[address]].fire() != None  and len(lista_bullet) == 0):
				b = lista_players[d[address]].fire()
				lista_players[d[address]].weapon.decAmmo()
				lista_bullet.extend(b)
		elif isinstance(data,Key_SPACE) and not lista_players[d[address]].AnimStart and not lista_players[d[address]].isJump:
			lista_players[d[address]].move_collide([0,-220],[platform.getHitBox() for platform in lista_platforms])
			lista_players[d[address]].isJump = True
		elif isinstance(data,No_Key):
			#lista_counters[d[address]] += 1
			if not lista_players[d[address]].AnimStart and lista_players[d[address]].getHealth() > 0:
				lista_players[d[address]].setStatus(2)

		if lista_players[d[address]].getHealth() <= 0:
			if not lista_players[d[address]].death:
				lista_players[d[address]].skin_counter = 0
			lista_players[d[address]].death = True
			lista_players[d[address]].skin_counter_to_return = lista_players[d[address]].lastSkinNumber() - 2
			lista_players[d[address]].setStatus(1)
			lista_players[d[address]].AnimStart = True
		
		lista_players[d[address]].updateHitBox()
		lista_players[d[address]].playAnimation()
		Gravita.apply(lista_players[d[address]],lista_platforms)
		lista_players[d[address]].setJump([platform.getHitBox() for platform in lista_platforms])

		lista_pickup_to_remove = list(lista_pickups)
		for pickup in lista_pickup_to_remove:
			pickup.updateHitBox()
			pickup.animation()
			if pickup.collide(lista_players[d[address]].getHitBox()):
				pickup.apply(lista_players[d[address]])
				pickup.time_picked = time.time()
				lista_pickups_respawn.append(lista_pickups.pop(lista_pickups.index(pickup)))
				break
			Gravita.apply(pickup,lista_platforms)

		for pickup in lista_pickups_respawn:
			if pickup.isRespwnable and time.time() - pickup.time_picked > pickup.time_to_spawn:
				lista_pickups.append(pickup)
				lista_pickups_respawn.remove(pickup)
				break

		lista_bullet_to_remove = list(lista_bullet)
		for bullet in lista_bullet_to_remove:
			bullet.updateHitBox()
			if bullet.getRange() > 0:
				bullet.move()
				bullet.decRange(bullet.getVelocity())
			if bullet.getRange() <= 0:
				lista_bullet.remove(bullet)
				break
			if lista_players[d[address]].collide(bullet.getHitBox()):
				lista_bullet.remove(bullet)
				lista_players[d[address]].decHealth(bullet.getDamage())
				break

		for platform in lista_platforms:
			if isinstance(platform,Elevator):
				platform.updateHitBox()
				platform.start()
		for trigerred in lista_trigerred:
			trigerred.setObjectCollide(lista_players[d[address]])
			trigerred.applyFunction(lista_players[d[address]],data)		
		
	elif isinstance(data,Recv):
		lista_to_send = list()
		lista_to_send.append(lista_players)
		lista_to_send.append(lista_platforms)
		lista_to_send.append(lista_pickups)
		lista_to_send.append(lista_bullet)
		lista_to_send.append(lista_trigerred)
		lista_to_send.append(lista_ghosts_platforms)
		send_udp((lista_to_send,lista_counters[d[address]]),address)

	elif type(data) == str:
		if data == "JOIN":
			if len(d) < NUMEBR_OF_PLAYERS:
				if not (address in d.keys()):
					d[address] = len(d)
					lista_players.append(player_selected(100,100))


while True:
	data , address = z.recvfrom(5120)
	thread = threading.Thread(target = handling_request , args=(data,address,))
	thread.start()