import socket
import pickle
import os
import time
import threading
from Timer import *
from Bullet import *
from Platform import *
from Map import *
from Pickup import *
from Queue import *
import sys

class Server():
    def paralell_managment(self):
        z = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        z.bind((self.ip,self.port_udp))
        while True:
            data , address = z.recvfrom(5120)
            if data.decode() == "atoma":
                z.sendto(f"{len(self.lista_users)}".encode('utf-8'),address)
                #print(f"{len(self.lista_users)}")
            elif data.decode() == "back":
                self.lista_users[0].close()
                self.lista_users.remove(self.lista_users[0])
            elif data.decode() == "check":
                z.sendto("1".encode(),address)

    def measure_ping(self):
        ping_socket = socket.socket()
        ping_socket.bind((self.ip,15001))
        ping_socket.listen()

        while True:
            connection , address = ping_socket.accept()
            print(f"Ping from {address}")

    def __init__(self,IP = "192.168.1.55",PORT_TCP = 15000,PORT_UDP = 20000):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.paralell_udp = threading.Thread(target=self.paralell_managment)
        self.paralell_ping = threading.Thread(target=self.measure_ping)
        self.ip = IP
        self.port_tcp = PORT_TCP
        self.port_udp = PORT_UDP
        self.map = MapCreator(open("maps/celani.txt")).returnMap()
        self.lista_users = list()
        self.lista_addresses = list()
        self.lista_bullet = [[],[]]
        self.lista_platforms = self.map.lista_bricks
        self.lista_powerups_objects = self.map.lista_powerups
        self.players_positions = [self.map.players_positions[0],self.map.players_positions[1]]
        self.information_for_players = [[100,510,100,False,100,0,0,0,0,0,False,10,False,False,0,0,False,False,False,0,10],
                                        [1200,510,200,False,100,0,0,0,0,0,False,10,False,False,0,0,False,False,False,0,10]]
        #self.lista_powerups = [False,False,False,False]
        self.lista_powerups_to_edit = [[],[]]
        self.timer1 = Timer(300)
        self.timer2 = Timer(200)
        self.udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.queue = Queue()
        self.flag_pickup = False
        self.time_to_spawn = 0
        self.lista_powerups_removed = list()

    def auto_start(self):
        self.start()
        self.wait_players()
        self.recv_informations()
        self.send_to_all_players(True)
        time.sleep(1)
        self.send_to_all_players(self.information_for_players)
        time.sleep(1)
        self.send_to_all_players(self.lista_powerups_objects)
        time.sleep(1)
        self.send_to_all_players(self.lista_bullet)
        time.sleep(1)
        self.send_to_all_players(self.lista_platforms)
        time.sleep(1)
        self.send_to_all_players("supreme")
        #time.sleep(1)
        #self.send_to_all_players(self.lista_powerups_objects)
        self.mainloop()
    
    def start(self):
        self.s.bind((self.ip,self.port_tcp))
        self.s.listen(2)
        print(f"Server Creato {self.ip}")

    def wait_players(self,max_number = 2):
        while len(self.lista_users) < max_number:
            connection , address = self.s.accept()
            self.lista_users.append(connection)
            self.lista_addresses.append(address)
            print(f"Si e connesso il {len(self.lista_users)}")
            self.lista_users[-1].send(pickle.dumps(len(self.lista_users)-1))

    

    def recv_informations(self):
        self.information_for_players[0] = pickle.loads(self.lista_users[0].recv(5120))
        self.information_for_players[0][0] = self.players_positions[0].x
        self.information_for_players[0][1] = self.players_positions[0].y

        self.information_for_players[1] = pickle.loads(self.lista_users[1].recv(5120))
        self.information_for_players[1][0] = self.players_positions[1].x
        self.information_for_players[1][1] = self.players_positions[1].y

    def send_to_all_players(self,lean):
        for user in self.lista_users:
            user.send(pickle.dumps(lean))
            

    def disconnect_all_players(self):
        for user in self.lista_users:
            user.close()

    def recv_udp(self,host):
        if self.queue.have_tail():
            index_packet =  self.queue.find_first(host)
            if index_packet != None:
                return self.queue.pick(index_packet)
            else:
                data = self.udp.recvfrom(5120)
                if data[1] != host:
                    self.queue.add(data)
                    self.recv_udp(host)
                else:
                    return data
        else:
            data = self.udp.recvfrom(5120)
            if data[1] != host:
                self.queue.add(data)
                self.recv_udp(host)
            else:
                return data

    def recv_udp2(self,host):
        return_packet = False
        while not return_packet:
            if self.queue.have_tail():
                index_packet =  self.queue.find_first(host)
                if index_packet != None:
                    return self.queue.pick(index_packet)
                else:
                    data = self.udp.recvfrom(5120)
                    if data[1] != host:
                        self.queue.add(data)
                        continue
                    return data    
            else:
                data = self.udp.recvfrom(5120)
                if data[1] != host:
                    self.queue.add(data)
                    continue
                else:
                    return data
     

    def send_upd(self,data,host):
        self.udp.sendto(pickle.dumps(data),host)

    def send_to_client(self,data,host):
        if pickle.loads(data)[1] == "info_player":
            self.information_for_players[int(self.d[host])] = pickle.loads(data)[0]
            self.send_upd(self.information_for_players,host)
        elif pickle.loads(data)[1] == "pickups":
            """
            self.lista_powerups_to_edit[int(self.d[host])] = pickle.loads(data)[0]
            try:
                for i in range(len(self.lista_powerups_to_edit[int(self.d[host])])):
                    try:
                        self.lista_powerups_objects[i].y = self.lista_powerups_to_edit[int(self.d[host])][i].y
                    except:
                        pass
                    if self.lista_powerups_to_edit[int(self.d[host])][i].getPick():
                        self.powerup_deleted = self.lista_powerups_objects.pop(i)
                        self.time_to_spawn = time.time()

                if self.time_to_spawn != 0:
                    if time.time() - self.time_to_spawn >= 5:
                        self.powerup_deleted.setPick(False)
                        self.lista_powerups_objects.append(self.powerup_deleted)
                        self.time_to_spawn = 0

                self.send_upd(self.lista_powerups_objects,host)
                print(f"{len(self.lista_powerups_objects)}")
            except:
                print("EXCEPTION PICKUPS")
                self.send_upd(self.lista_powerups_to_edit[int(self.d[host])],host)
            """
            powerups_to_remove = pickle.loads(data)[0]

            for i in range(len(self.lista_powerups_objects)):
                for j in range(len(powerups_to_remove)):
                    if self.lista_powerups_objects[i] == powerups_to_remove[j]:
                        self.lista_powerups_removed.append(self.lista_powerups_objects.pop(i))  
                        self.time_to_spawn = time.time()  
                        break

            if self.time_to_spawn != 0:
                if time.time() - self.time_to_spawn >= 5:
                    self.lista_powerups_objects.append(self.lista_powerups_removed[-1])
                    self.time_to_spawn = 0

            self.send_upd(self.lista_powerups_objects,host)

        elif pickle.loads(data)[1] == "bullets":
            self.lista_bullet[int(self.d[host])] = pickle.loads(data)[0]
            for ID in range(2):
                for i in self.lista_bullet[ID]:
                    print(i.getRange())
                    if(i.getRange() > 0):
                        i.move()
                        i.decRange(i.getVelocity())

            self.send_upd(self.lista_bullet,host)

    def mainloop(self):
        self.udp.bind(("192.168.1.55",23005))

        self.d = {}
        while len(self.d) < 2:
            info = self.udp.recvfrom(8192)
            if info[1] not in self.d.keys():
                self.d[info[1]] = str(info[0].decode())

        d = dict(sorted(self.d.items() , key= lambda x: x[1]))


        for host in list(d.keys()):
            self.send_upd("Ready",host)

        print(d)
        while True:
            try:
                data , host = self.udp.recvfrom(5120)
                t = threading.Thread(target=self.send_to_client,args=(data,host))
                t.start()
            except Exception as e:
                print(e)
                print(sys.exc_info()[-1].tb_lineno)
                self.disconnect_all_players()
                self.s.close()
                self.__init__()
                self.auto_start()

if __name__ == "__main__":
    server = Server()
    server.paralell_udp.start()
    server.paralell_ping.start()
    server.auto_start()    
