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

class Server:
    map_dict = Map.loadMap("lavanuova")
    MAX_NUMEBR_OF_PLAYERS = 2
    lista_initial_positions = [map_dict['Player'][0],map_dict['Player'][1]]
    lista_players = list()
    lista_platforms =  list(map_dict['Platform'])
    lista_pickups = list(map_dict['Pickup'])
    lista_pickups_respawn = list()
    lista_bullet = list()
    lista_trigerred = list(map_dict['Trigger'])
    lista_ghosts_platforms = list(map_dict['Ghosts'])
    lista_endgame = list([])
    z = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    lista_counters = [0,0]
    lista_time_to_respond = [0,0]
    d = dict()

    @classmethod
    def reset(cls, restart_dict = True):
        cls.lista_initial_positions = [cls.map_dict['Player'][0],cls.map_dict['Player'][1]]
        cls.lista_players = list()
        cls.lista_platforms =  list(cls.map_dict['Platform'])
        cls.lista_pickups = list(cls.map_dict['Pickup'])
        cls.lista_pickups_respawn = list()
        cls.lista_bullet = list()
        cls.lista_trigerred = list(cls.map_dict['Trigger'])
        cls.lista_ghosts_platforms = list(cls.map_dict['Ghosts'])
        cls.lista_endgame = list([])
        cls.lista_counters = [0,0]
        cls.lista_time_to_respond = [0,0]
        if restart_dict:
            cls.d = dict()

    @classmethod
    def __send_udp(cls,data,address):
	    Server.z.sendto(pickle.dumps(data),address)

    @classmethod
    def handling_request(cls,data,address):
        try:
            data = pickle.loads(data)
        except Exception as e:
            print("EXCEPTION PICKLE ",e)
            return

        if type(data) == tuple:
            if type(data[0]) == str and issubclass(data[1],Player):
                data , player_selected = data
            else:
                data , counter = data
        if address in cls.d:
            cls.lista_time_to_respond[cls.d[address]] = time.time()
            if isinstance(data,Commands):
                if counter != None:
                    Server.lista_counters[Server.d[address]] = counter
                if isinstance(data,Key_D) and not Server.lista_players[Server.d[address]].AnimStart:
                    Server.lista_players[Server.d[address]].setStatus(0)
                    Server.lista_players[Server.d[address]].setSide(1)
                    Server.lista_players[Server.d[address]].move_collide([20,0],[platform.getHitBox() for platform in Server.lista_platforms])
                    #print(f"{address} Press D")
                elif isinstance(data,Key_A) and not Server.lista_players[Server.d[address]].AnimStart:
                    Server.lista_players[Server.d[address]].setStatus(0)
                    Server.lista_players[Server.d[address]].setSide(0)
                    Server.lista_players[Server.d[address]].move_collide([-20,0],[platform.getHitBox() for platform in Server.lista_platforms])
                    #print(f"{address} Press A")
                elif isinstance(data,Key_W):
                    Server.lista_players[Server.d[address]].move_collide([0,-10],[platform.getHitBox() for platform in Server.lista_platforms])
                    #lista_platforms.remove(lista_platforms[-1])
                elif isinstance(data,Key_S):
                    Server.lista_players[Server.d[address]].move_collide([0,10],[platform.getHitBox() for platform in Server.lista_platforms])
                elif isinstance(data,Key_V)  and not Server.lista_players[Server.d[address]].AnimStart:
                    Server.lista_players[Server.d[address]].skin_counter = 0
                    Server.lista_players[Server.d[address]].setStatus(4)
                    Server.lista_players[Server.d[address]].AnimStart = True
                elif isinstance(data,Key_L):
                    if(Server.lista_players[Server.d[address]].fire() != None  and len(Server.lista_bullet) == 0):
                        b = Server.lista_players[Server.d[address]].fire()
                        Server.lista_players[Server.d[address]].weapon.decAmmo()
                        Server.lista_bullet.extend(b)
                elif isinstance(data,Key_SPACE) and not Server.lista_players[Server.d[address]].AnimStart and not Server.lista_players[Server.d[address]].isJump:
                    Server.lista_players[Server.d[address]].move_collide([0,-220],[platform.getHitBox() for platform in Server.lista_platforms])
                    Server.lista_players[Server.d[address]].isJump = True
                elif isinstance(data,No_Key):
                    if not Server.lista_players[Server.d[address]].AnimStart and Server.lista_players[Server.d[address]].getHealth() > 0:
                        Server.lista_players[Server.d[address]].setStatus(2)

                if Server.lista_players[Server.d[address]].getHealth() <= 0:
                    if not Server.lista_players[Server.d[address]].death:
                        Server.lista_players[Server.d[address]].skin_counter = 0
                    Server.lista_players[Server.d[address]].death = True
                    Server.lista_players[Server.d[address]].skin_counter_to_return = Server.lista_players[Server.d[address]].lastSkinNumber() - 2
                    Server.lista_players[Server.d[address]].setStatus(1)
                    Server.lista_players[Server.d[address]].AnimStart = True
                    if Server.lista_players[Server.d[address]].skin_counter == Server.lista_players[Server.d[address]].lastSkinNumber() - 2:
                        print("--------------------ENDGAME-------------")
                        if len(cls.lista_endgame) == 0:
                            cls.lista_endgame.append(True)
                            lista_to_send = list()
                            lista_to_send.append(Server.lista_players)
                            lista_to_send.append(Server.lista_platforms)
                            lista_to_send.append(Server.lista_pickups)
                            lista_to_send.append(Server.lista_bullet)
                            lista_to_send.append(Server.lista_trigerred)
                            lista_to_send.append(Server.lista_ghosts_platforms)
                            lista_to_send.append(Server.lista_endgame)
                            for addresses in cls.d.keys():
                                cls.__send_udp((lista_to_send,Server.lista_counters[Server.d[address]]),addresses)
                            cls.reset()
                            return

                
                Server.lista_players[Server.d[address]].updateHitBox()
                Server.lista_players[Server.d[address]].playAnimation()
                Gravita.apply(Server.lista_players[Server.d[address]],Server.lista_platforms)
                Server.lista_players[Server.d[address]].setJump([platform.getHitBox() for platform in Server.lista_platforms])

                lista_pickup_to_remove = list(Server.lista_pickups)
                for pickup in lista_pickup_to_remove:
                    pickup.updateHitBox()
                    pickup.animation()
                    if pickup.collide(Server.lista_players[Server.d[address]].getHitBox()):
                        pickup.apply(Server.lista_players[Server.d[address]])
                        pickup.time_picked = time.time()
                        Server.lista_pickups_respawn.append(Server.lista_pickups.pop(Server.lista_pickups.index(pickup)))
                        break
                    Gravita.apply(pickup,Server.lista_platforms)

                for pickup in Server.lista_pickups_respawn:
                    if pickup.isRespwnable and time.time() - pickup.time_picked > pickup.time_to_spawn:
                        Server.lista_pickups.append(pickup)
                        Server.lista_pickups_respawn.remove(pickup)
                        break

                lista_bullet_to_remove = list(Server.lista_bullet)
                for bullet in lista_bullet_to_remove:
                    bullet.updateHitBox()
                    if bullet.getRange() > 0:
                        bullet.move()
                        bullet.decRange(bullet.getVelocity())
                    if bullet.getRange() <= 0:
                        Server.lista_bullet.remove(bullet)
                        break
                    if Server.lista_players[Server.d[address]].collide(bullet.getHitBox()):
                        Server.lista_bullet.remove(bullet)
                        Server.lista_players[Server.d[address]].decHealth(bullet.getDamage())
                        break

                for platform in Server.lista_platforms:
                    if isinstance(platform,Elevator):
                        platform.updateHitBox()
                        platform.start()
                for trigerred in Server.lista_trigerred:
                    trigerred.setObjectCollide(Server.lista_players[Server.d[address]])
                    trigerred.applyFunction(Server.lista_players[Server.d[address]],data)		
                
            if isinstance(data,Exit):
                if len(cls.lista_endgame) == 0:
                    cls.lista_endgame.append(True)
                    lista_to_send = list()
                    lista_to_send.append(Server.lista_players)
                    lista_to_send.append(Server.lista_platforms)
                    lista_to_send.append(Server.lista_pickups)
                    lista_to_send.append(Server.lista_bullet)
                    lista_to_send.append(Server.lista_trigerred)
                    lista_to_send.append(Server.lista_ghosts_platforms)
                    lista_to_send.append(Server.lista_endgame)
                    for addresses in cls.d.keys():
                        cls.__send_udp((lista_to_send,Server.lista_counters[Server.d[address]]),addresses)
                    cls.reset()
                    return

        if isinstance(data,Recv):
            lista_to_send = list()
            lista_to_send.append(Server.lista_players)
            lista_to_send.append(Server.lista_platforms)
            lista_to_send.append(Server.lista_pickups)
            lista_to_send.append(Server.lista_bullet)
            lista_to_send.append(Server.lista_trigerred)
            lista_to_send.append(Server.lista_ghosts_platforms)
            lista_to_send.append(Server.lista_endgame)
            try:
                cls.__send_udp((lista_to_send,Server.lista_counters[Server.d[address]]),address)
            except:
                pass

        elif type(data) == str:
            if data == "JOIN":
                if len(cls.d) < cls.MAX_NUMEBR_OF_PLAYERS:
                    if not (address in cls.d.keys()):
                        cls.d[address] = len(cls.d)
                        cls.lista_players.append(player_selected(cls.lista_initial_positions[cls.d[address]].x,cls.lista_initial_positions[cls.d[address]].y))
                        print(f"Connected {address}")
                        cls.__send_udp(cls.d[address],address)
                        cls.lista_time_to_respond[cls.d[address]] = time.time()
                        cls.lista_pickups = list(cls.map_dict['Pickup'])
                        for i in range(len(cls.lista_players)):
                            cls.lista_players[i].__init__(cls.lista_initial_positions[i].x,cls.lista_initial_positions[i].y)
                else:
                    cls.__send_udp(False,address)
            elif data == "Nplayers":
                cls.__send_udp(len(cls.d),address)


    @classmethod
    def start(cls):
        cls.z.bind(("192.168.1.55",20001))
        print("SERVER HAS BEEN STARTING LISTENING ON ADDRESS 192.168.1.55:20000")
        while True:
            for time_respond in cls.lista_time_to_respond:
                if time_respond != 0:
                    if time.time() - time_respond > 5:
                        if len(cls.lista_endgame) == 0:
                            cls.lista_endgame.append(True)
                            lista_to_send = list()
                            lista_to_send.append(Server.lista_players)
                            lista_to_send.append(Server.lista_platforms)
                            lista_to_send.append(Server.lista_pickups)
                            lista_to_send.append(Server.lista_bullet)
                            lista_to_send.append(Server.lista_trigerred)
                            lista_to_send.append(Server.lista_ghosts_platforms)
                            lista_to_send.append(Server.lista_endgame)
                            for addresses in cls.d.keys():
                                cls.__send_udp((lista_to_send,10000),addresses)
                            cls.reset()
                            break
            data , address = cls.z.recvfrom(5120)
            thread = threading.Thread(target = cls.handling_request , args=(data,address,))
            thread.start()

if __name__ == "__main__":
    Server.start()    