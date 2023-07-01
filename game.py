import pygame
from graph import *
import socket
import pickle
import os
import time
from function import *
from message import *
from menu_gameplay import *
from player_model import *
from triangle import *
from player import *
from Platform import *
from Gravita import *
from Timer import *
import random
import ObjectInGame
from ImageButton import *
from InteractiveImageButton import *
from SwitchButton import *
from Sliders import *
from labels import *
from Scroller import *
from Bullet import *
from LifeBar import *
from Music import *
from Pickup import *
from Background import *
import threading
from FCommands import *
import concurrent.futures
from FrecvDataFactory import RecvDataFactory
from TrigerredZone import *

class Game():
	def __init__(self,name,windowSize,FPS):
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption((str(name)))
		self.version = "1.3.0"
		self.windowSize = windowSize
		self.z = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.center_server_informations = ("2.85.253.85",20099)
		self.background_color = (27,37,48)
		self.ID_PLAYER = None
		self.win = pygame.display.set_mode(windowSize, pygame.SCALED) 
		#self.win = pygame.display.set_mode(windowSize,pygame.FULLSCREEN | pygame.SCALED)
		self.isFullScreen = False
		self.isMusicOn = True
		ObjectInGame.win = self.win
		self.clock = pygame.time.Clock()
		self.FPS = FPS

		self.run_game = True
		self.run_menu = True
		self.run_options = False
		self.run_show_keys = False
		self.run_select_mode = False
		self.run_menu_select_player = False
		self.run_menu_connect_to_server = False
		self.run_gameplay  = False
		self.run_podio = False
		self.wait_players = False

		self.font_comic_sans = pygame.font.SysFont('Comic Sans MS', 60)
		self.lista_menus = pygame.sprite.Group()

		Music.background_instrumental.play()

	def send_udp(self,data,address):
		self.z.sendto(pickle.dumps(data),address)  

	def recv_udp(self,buffer_size = 5120):
		try:
			return pickle.loads(self.z.recvfrom(buffer_size)[0])
		except:
			return None     

	def load(self):
		self.counter = 0
		self.lista_queue = list()
		self.counter_server = 0
		self.lista_players = list()
		self.lista_platforms = list()
		self.lista_pickups = list()
		self.lista_bullet = list()
		self.lista_trigerred = list()
		self.lista_ghosts_platforms = list()

		self.no_image = pygame.image.load("HUD/no_image.png")

		self.win.fill(self.background_color)

		pygame.display.update()

		self.loading_images = ricevi_foto("/loading_images")

		self.gameplay_background_image = pygame.image.load("background__001.png")

		self.image_start_button = ricevi_foto("/start_button")

		self.image_switch_button = ricevi_foto("/sound_button")

		self.image_exit_button = ricevi_foto("/exit_button")

		self.image_options_button = ricevi_foto("/options_button")

		self.image_back_button = ricevi_foto("/back_button")

		self.image_next_button = ricevi_foto("/next_button")

		self.image_right_arrow = ricevi_foto("/arrows")[1]

		self.image_left_arrow = ricevi_foto("/arrows")[0]

		self.image_full_screen = ricevi_foto("/full_screen_image")

		self.image_sounds = ricevi_foto("/sounds_image")

		self.image_base = ricevi_foto("/select_player_images")[1]

		self.arrow_up_button_image = pygame.image.load("connect_to_server_images/arrow_up.png")

		self.arrow_down_button_image = pygame.image.load("connect_to_server_images/arrow_down.png")

		self.reload_button_image = pygame.image.load("connect_to_server_images/reload.png")

		self.win_image = Image(456,30,pygame.image.load('podio/winner.png'))

		self.loser_image = Image(456,30,pygame.image.load('podio/loser.png'))

		self.class_players = [Supreme,SferaEbbasta,TonyEffe,Fedez,SocialBoom]

		triangles = ricevi_foto("/triangle")
		self.triangle_left = triangles[0]
		self.triangle_right = triangles[1]

	def recv_and_update(self):
		self.send_udp((Recv(),None),self.server_udp_informations)
		last_server = self.counter_server
		try:
			recv_data , counter_server = self.recv_udp()
		except Exception as e:
			recv_data = None
			print("Exception Recv Data")

		if recv_data != None:
			lista_players_new = RecvDataFactory.getRecvData(recv_data,Player,self.lista_players)
			if counter_server >= last_server:
				for i in range(counter_server,self.counter):
					if isinstance(self.lista_queue[i][0],Key_D):
						#print("Key D Prediction")
						if not lista_players_new[self.ID_PLAYER].AnimStart:
							lista_players_new[self.ID_PLAYER].setStatus(0)
							lista_players_new[self.ID_PLAYER].setSide(1)
							lista_players_new[self.ID_PLAYER].move_collide([20,0],[platform.getHitBox() for platform in self.lista_platforms])
							if lista_players_new[self.ID_PLAYER].hitBox.right > 1360:
								lista_players_new[self.ID_PLAYER].move_to(pygame.Vector2(0,lista_players_new[self.ID_PLAYER].y))
					if isinstance(self.lista_queue[i][0],Key_A):
						#print("Key A Prediction")
						if not lista_players_new[self.ID_PLAYER].AnimStart:
							lista_players_new[self.ID_PLAYER].setStatus(0)
							lista_players_new[self.ID_PLAYER].setSide(0)
							lista_players_new[self.ID_PLAYER].move_collide([-20,0],[platform.getHitBox() for platform in self.lista_platforms])
							if lista_players_new[self.ID_PLAYER].hitBox.left < 0:
								lista_players_new[self.ID_PLAYER].hitBox.right = 1360
								lista_players_new[self.ID_PLAYER].move_to(pygame.Vector2(lista_players_new[self.ID_PLAYER].hitBox.x,lista_players_new[self.ID_PLAYER].y))
					if isinstance(self.lista_queue[i][0],Key_SPACE):
						lista_players_new[self.ID_PLAYER].move_collide([0,-220],[platform.getHitBox() for platform in self.lista_platforms])
						lista_players_new[self.ID_PLAYER].isJump = True
					if isinstance(self.lista_queue[i][0],Key_W):
						lista_players_new[self.ID_PLAYER].move_collide([0,-10],[platform.getHitBox() for platform in self.lista_platforms])
					if isinstance(self.lista_queue[i][0],Key_S):
						lista_players_new[self.ID_PLAYER].move_collide([0,10],[platform.getHitBox() for platform in self.lista_platforms])
					if isinstance(self.lista_queue[i][0],Key_V):
						lista_players_new[self.ID_PLAYER].skin_counter = 0
						lista_players_new[self.ID_PLAYER].setStatus(4)
						lista_players_new[self.ID_PLAYER].AnimStart = True
					if isinstance(self.lista_queue[i][0],No_Key):
						if not lista_players_new[self.ID_PLAYER].AnimStart and lista_players_new[self.ID_PLAYER].getHealth() > 0:
							lista_players_new[self.ID_PLAYER].setStatus(2)
					if self.lista_queue[i][0] == Gravita:
						#print("ON GRAVITA")
						Gravita.apply(lista_players_new[self.ID_PLAYER],self.lista_platforms)
						lista_players_new[self.ID_PLAYER].setJump([platform.getHitBox() for platform in self.lista_platforms])

				self.lista_players = list(lista_players_new)
			
			self.lista_platforms = RecvDataFactory.getRecvData(recv_data,Platform,self.lista_platforms)
			self.lista_pickups = RecvDataFactory.getRecvData(recv_data,Pickup,self.lista_pickups)
			self.lista_bullet = RecvDataFactory.getRecvData(recv_data,Bullet,self.lista_bullet)
			self.lista_trigerred = RecvDataFactory.getRecvData(recv_data,TrigerredZone,self.lista_trigerred)
			self.lista_ghosts_platforms = RecvDataFactory.getRecvData(recv_data,GhostPlatform,self.lista_ghosts_platforms)
			self.end_game =  RecvDataFactory.getRecvData(recv_data,bool,self.end_game)

	def allScenesFalse(self):
		self.run_menu = False
		self.run_select_mode = False
		self.run_options = False
		self.run_show_keys = False
		self.run_menu_select_player = False
		self.run_menu_connect_to_server = False
		self.run_gameplay  = False
		self.run_podio = False
		self.wait_players = False

	def menu(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		self.counter = 0
		self.lista_queue = list()
		self.counter_server = 0
		self.lista_players = list()
		self.lista_platforms = list()
		self.lista_pickups = list()
		self.lista_bullet = list()
		self.lista_trigerred = list()
		self.lista_ghosts_platforms = list()

		start_button = InteractiveImageButton(int(widthScreen/2),int(HeightScreen*0.26),self.image_start_button[0],self.image_start_button[1],Music.click) 

		options_button = InteractiveImageButton(int(widthScreen/2),int(HeightScreen*0.45),self.image_options_button[0],self.image_options_button[1],Music.click)

		exit_button = InteractiveImageButton(int(widthScreen/2),int(HeightScreen*0.65),self.image_exit_button[0],self.image_exit_button[1],Music.click)

		can_touch_buttons = False

		while self.run_menu:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run_game = False
					self.allScenesFalse()

			if Music.background_instrumental.get_num_channels() == 0:
				Music.background_instrumental.play()

			if not pygame.mouse.get_pressed()[0]:
				can_touch_buttons = True

			keys = pygame.key.get_pressed()

			self.win.fill(self.background_color)
			

			start_button.spawn()

			if start_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_select_mode = True

			options_button.spawn()

			if options_button.clicked() and can_touch_buttons :
				self.allScenesFalse()
				self.run_options = True

			exit_button.spawn()

			if exit_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_game = False

			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def select_mode(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		back_button = ImageButton(widthScreen*0.05,80,self.image_back_button[0],Music.click)

		story_button = ImageButton(int(widthScreen/2),int(HeightScreen*0.26),pygame.image.load("select_mode_scene/story_button/story_button.png"),Music.click)

		online_button = InteractiveImageButton(int(widthScreen/2),int(HeightScreen*0.45),pygame.image.load("select_mode_scene/online_button/no_over.png"),pygame.image.load("select_mode_scene/online_button/over.png"),Music.click)

		can_touch_buttons = False

		while self.run_select_mode:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run_game = False
					self.run_select_mode = False

			self.win.fill(self.background_color)

			if not pygame.mouse.get_pressed()[0]:
				can_touch_buttons = True

			back_button.spawn()

			if back_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_menu = True      

			story_button.spawn()  

			online_button.spawn()

			if online_button.clicked() and can_touch_buttons:
				try:
					self.z.settimeout(3)
					self.z.sendto("version".encode(),self.center_server_informations)
					response = self.z.recvfrom(5120)[0].decode()
					if response == self.version:
						self.allScenesFalse()
						self.run_menu_select_player = True
					else:
						self.allScenesFalse()
						self.run_menu = True
						self.lista_menus.add(UpdateMessage((int(widthScreen/2),int(HeightScreen/2)-30), self.win))

				except:
					self.allScenesFalse()
					self.run_menu = True
					self.lista_menus.add(ConnectionErrorr((int(widthScreen/2),int(HeightScreen/2)-50), self.win))
				self.z.settimeout(None)

			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def options(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		back_button = ImageButton(widthScreen*0.05,80,self.image_back_button[0],Music.click)

		keys_button = ImageButton(int(widthScreen/2)+20,500,pygame.image.load("options_button/ButtonViewKeys.png"),Music.click)

		full_screen_switch_button = SwitchButton(int(widthScreen/2)+220,300,self.image_switch_button[0],self.image_switch_button[1],Music.click)
		full_screen_switch_button.status = self.isFullScreen

		switch_button = SwitchButton(int(widthScreen/2)+220,400,self.image_switch_button[1],self.image_switch_button[0],Music.click)
		switch_button.status = not self.isMusicOn

		can_touch_buttons = False

		while self.run_options:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run_menu = False

			self.win.fill(self.background_color)

			if not pygame.mouse.get_pressed()[0]:
				can_touch_buttons = True


			back_button.spawn()

			if back_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_menu = True


			self.win.blit(self.image_full_screen[0],(self.image_full_screen[0].get_rect(center = (int(widthScreen/2)-50,300))))

			self.win.blit(self.image_sounds[0],(self.image_full_screen[0].get_rect(center = (int(widthScreen/2)-50,400))))

			full_screen_switch_button.spawn()

			if full_screen_switch_button.clicked() and can_touch_buttons:

				if full_screen_switch_button.status:
					self.win = pygame.display.set_mode(self.windowSize,pygame.FULLSCREEN)
					self.isFullScreen = True
				else:
					self.win = pygame.display.set_mode(self.windowSize)
					self.isFullScreen = False

				widthScreen = self.win.get_rect()[2]
				HeightScreen = self.win.get_rect()[3]

				back_button = ImageButton(widthScreen*0.05,80,self.image_back_button[0],Music.click)

				full_screen_switch_button = SwitchButton(int(widthScreen/2)+220,300,self.image_switch_button[0],self.image_switch_button[1],Music.click)
				full_screen_switch_button.status = self.isFullScreen

				switch_button = SwitchButton(int(widthScreen/2)+220,400,self.image_switch_button[1],self.image_switch_button[0],Music.click)

			switch_button.spawn()

			if switch_button.clicked() and can_touch_buttons:
				if switch_button.status:
					Music.change_volume(0)
					#pygame.mixer.pause()
					self.isMusicOn = False
				else:
					Music.change_volume(0.6)
					#pygame.mixer.unpause()
					self.isMusicOn = True

			keys_button.spawn()

			if keys_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_show_keys = True

			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def show_keys(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		back_button = ImageButton(widthScreen*0.05,80,self.image_back_button[0],Music.click)

		keys_image = Image(int(widthScreen/2),int(HeightScreen/2),pygame.image.load("options_button/keys.png"))

		can_touch_buttons = False

		while self.run_show_keys:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run_menu = False

			self.win.fill(self.background_color)

			if not pygame.mouse.get_pressed()[0]:
				can_touch_buttons = True

			back_button.spawn()

			if back_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_options = True

			keys_image.spawn()


			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def select_player(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		sfera_model_skins = ricevi_foto("/characters/sfera_ebbasta/model")
		tony_model_skins = ricevi_foto("/characters/tony_effe/model")
		supreme_model_skins = ricevi_foto("/characters/supreme/model")
		fedez_model_skins = ricevi_foto("/characters/fedez/model")
		social_boom_model_skins = ricevi_foto("/characters/social_boom/model")

		back_button = ImageButton(widthScreen*0.05,80,self.image_back_button[0],Music.click)

		next_button = ImageButton(widthScreen*0.95,80,self.image_next_button[0],Music.click)

		self.index = 0

		left_button = ImageButton(int(widthScreen/2)-300,int(HeightScreen/2),self.image_left_arrow,Music.click)

		right_button = ImageButton(int(widthScreen/2)+300,int(HeightScreen/2),self.image_right_arrow,Music.click)

		player_slider = ButtonSlider(int(widthScreen/2),int(HeightScreen/2),list([supreme_model_skins,sfera_model_skins,tony_model_skins,fedez_model_skins,social_boom_model_skins]),left_button,right_button)

		can_touch_buttons = False

		while self.run_menu_select_player:
			self.clock.tick(self.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.allScenesFalse()
					self.run_game = False


			self.win.fill(self.background_color)

			if not pygame.mouse.get_pressed()[0]:
				can_touch_buttons = True

			next_button.spawn()

			if next_button.clicked():
				self.index = player_slider.getIndex()
				self.allScenesFalse()
				self.run_menu_connect_to_server = True

			back_button.spawn()

			if back_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_select_mode = True

			
			self.win.blit(self.image_base,self.image_base.get_rect(center = (int(widthScreen/2),int(HeightScreen/2)+200)))
			player_slider.spawn()


			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def connect_to_server(self):
		self.z.settimeout(1)

		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		back_button = ImageButton(widthScreen*0.05,80,self.image_back_button[0],Music.click)

		arrow_up_button = ImageButton(int(widthScreen/1.133333),int(HeightScreen/7.68),self.arrow_up_button_image,Music.click)

		arrow_down_button = ImageButton(int(widthScreen/1.133333),int(HeightScreen/1.0971),self.arrow_down_button_image,Music.click)

		reload_button = ImageButton(int(widthScreen/1.36),int(HeightScreen/7.68),self.reload_button_image,Music.click)

		lista_texts = [
				Text(0,0,"SERVER ",30,self.win),
				Text(0,0,"PORT ",30,self.win),
				Text(0,0,"PLAYERS",30,self.win)
					]

		texts_label = Label(int(widthScreen/3.88),int(HeightScreen/7.68),lista_texts,140,self.win)

		self.z.sendto("Servers".encode(),self.center_server_informations)
		Servers = pickle.loads(self.z.recvfrom(5120)[0])

		server_labels = list()

		for server in Servers:
			server_labels.append(ServerLabel(200,200,str(server[0]),str(server[1]),str(server[2]),0))

		server_labels2 = [
				ServerLabel(200,200,"94.68.41.227","15000","20000",0),
				ServerLabel(200,350,"94.69.177.240","15000","20000",1),
				ServerLabel(200,350,"192.168.1.3","15003","20003",1)
						]

		server_scroller = Scroller(int(widthScreen/1.942),int(HeightScreen/3.84),server_labels,3,self.win)

		for server in server_scroller.lista_objects:
			try:
				self.z.sendto(pickle.dumps("Nplayers"),(str(server.ip.text),int(server.port_udp)))
				response , data = self.z.recvfrom(5120)
				server.status = True
			except:
				server.status = False

		can_touch_buttons = False

		while self.run_menu_connect_to_server:
			self.clock.tick(self.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.allScenesFalse()
					self.run_game = False

			keys = pygame.key.get_pressed()

			self.win.fill(self.background_color)

			if not pygame.mouse.get_pressed()[0]:
				can_touch_buttons = True

			back_button.spawn()

			if back_button.clicked() and can_touch_buttons:
				self.allScenesFalse()
				self.run_menu_select_player = True

			index = 0
			online_servers_counter = 0
			for server in server_scroller.lista_objects:
				if server.status:
					online_servers_counter += 1
					try:
						self.z.sendto(pickle.dumps("Nplayers"),(str(server.ip.text),int(server.port_udp)))
						number_of_players = str(int(pickle.loads(self.z.recvfrom(5120)[0])))
						server.setNumberOfPlayers(number_of_players)

						if int(server.players.text) < 2:
							if server.connect_button.clicked():

								self.ip_to_connect = str(server.ip.text)
								self.port_udp = int(server.port_udp)
								self.server_udp_informations = (self.ip_to_connect,self.port_udp)

								self.send_udp(("JOIN",self.class_players[self.index]),self.server_udp_informations)

								self.ID_PLAYER , self.background_name = self.recv_udp()
								self.ID_PLAYER = int(self.ID_PLAYER)
								self.end_game = []

								self.send_udp((Recv(),None),self.server_udp_informations)
								self.recv_and_update()

								time.sleep(1)

								self.allScenesFalse()
								self.wait_players = True
					except Exception as e:
						server.status = False
						print(f"kati pige lathos   {e}")
			texts_label.spawn()

			server_scroller.spawn()
			
			if online_servers_counter > 3:
				if arrow_down_button.clicked():
					server_scroller.scrollDown()

				if arrow_up_button.clicked():
					server_scroller.scrollUp()

				arrow_down_button.spawn()

				arrow_up_button.spawn()

			reload_button.spawn()

			if reload_button.clicked():
				for server in server_scroller.lista_objects:
					try:
						self.z.sendto(pickle.dumps("Nplayers"),(str(server.ip.text),int(server.port_udp)))
						response , data = self.z.recvfrom(5120)
						server.status = True
					except Exception as e:
						print(e)
						server.status = False

			if keys[pygame.K_r]:
				for server in server_scroller.lista_objects:
					try:
						self.z.sendto(pickle.dumps("Nplayers"),(str(server.ip.text),int(server.port_udp)))
						response , data = self.z.recvfrom(5120)
						server.status = True
					except Exception as e:
						print(e)
						server.status = False
				
			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def wait_players_to_play(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		self.loading_image = Image(int(widthScreen/2),int(HeightScreen/2),pygame.image.load("loading_images/LOADING.png"))

		while self.wait_players:
			self.clock.tick(self.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.allScenesFalse()
					self.run_game = False
			keys = pygame.key.get_pressed()

			self.win.fill(self.background_color)

			self.loading_image.spawn()

			pygame.display.update()


			self.background = Background(self.background_name)
			self.allScenesFalse()
			self.run_gameplay = True

			

			self.lista_menus.draw(self.win)
			self.lista_menus.update()

	def handling(self,send_objects,pickups,lista_bullet):
		server_udp_informations = (("94.68.80.49",23005))
		while True:
			try:
				send_objects.sendto(pickle.dumps([self.information_for_players[self.ID],"info_player"]),server_udp_informations)
				self.information_for_players = list(pickle.loads(send_objects.recvfrom(5120)[0]))

				send_objects.sendto(pickle.dumps([pickups,"pickups"]),server_udp_informations)
				self.second_pickups = list(pickle.loads(send_objects.recvfrom(5120)[0]))

				send_objects.sendto(pickle.dumps([lista_bullet[self.ID],"bullets"]),server_udp_informations)
				self.send_lista_bullet = list(pickle.loads(send_objects.recvfrom(5120)[0]))
			except Exception as e:
				print(e)
	
	def play(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		self.wait_players_message = WaitPlayerMessage((int(widthScreen/2)+50,int(HeightScreen/2)-300), self.win)

		Music.background_instrumental.fadeout(300)

		progress_bars = [LifeBar(150,50,"THE OTHER PLAYER",self.no_image,100),
						LifeBar(1150,50,"THE OTHER PLAYER",self.no_image,100)]

		self.winner = True 

		if len(self.lista_players) < 2:
			self.lista_menus.add(self.wait_players_message)
	   
		while self.run_gameplay:
			self.z.settimeout(6)
			self.no_key = True
			self.clock.tick(self.FPS)

			if Music.desert.get_num_channels() == 0:
				Music.desert.play() 

			threading.Thread(target= self.recv_and_update).start()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					#self.send_udp(Exit(),self.server_udp_informations)
					self.allScenesFalse()
					self.background = None
			keys = pygame.key.get_pressed()

			if len(self.lista_players) == 2 and self.lista_menus.has(self.wait_players_message):
				self.lista_menus.empty()
				

			for reason in self.end_game:
				if reason:
					if self.lista_players[self.ID_PLAYER].getHealth() > 0:
						self.winner = True
					elif self.lista_players[self.ID_PLAYER].getHealth() <= 0:
						self.winner = False
					
					Music.desert.fadeout(300)
					self.allScenesFalse()
					self.run_podio = True
					self.lista_menus.empty()

			self.win.fill((255,200,20))

			self.background.spawn(self.win)

			try: 
				for player in self.lista_players:
					player.spawn(self.win)
			except Exception as e:
				print(e)

			for platform in self.lista_platforms:
				platform.spawn(self.win)

			for pickup in self.lista_pickups:
				pickup.spawn(self.win)
				for player in self.lista_players:
					if pickup.collide(player.hitBox):
						Music.pick_powerup.play()
				#		if pickup.hasEffect:
				#			self.lista_menus.add(pickup.effect(player.position.elementwise() - 40,self.win))
				

			for bullet in self.lista_bullet:
				bullet.spawn()
				for player in self.lista_players:
					if bullet.collide(player.hitBox):
						self.lista_menus.add(Blood((bullet.x,bullet.y),self.win))
						Music.collision.play()
				for platform in self.lista_platforms:
					if bullet.collide(platform.hitBox):
						self.lista_menus.add(Hit((bullet.x,bullet.y),self.win))
						Music.collision.play()
			
			for trigerred in self.lista_trigerred:
				#trigerred.spawn(self.win) FOR TRAILER
				pass

			for ghost in self.lista_ghosts_platforms:
				ghost.spawn(self.win)

			
			for ID in range(len(self.lista_players)):
				for ID_ in range(len(progress_bars)):
					if self.lista_players[ID].collide(progress_bars[ID_].hitBox):
						progress_bars[ID_].move([0,-30])
					elif not self.lista_players[ID].collide(progress_bars[ID_].hitBox) and progress_bars[ID_].y <= 50:
						progress_bars[ID_].move([0,1])
			


			for ID in range(len(self.lista_players)): 
				progress_bars[ID].setBullets(self.lista_players[ID].weapon.getAmmo())
				progress_bars[ID].setLife(self.lista_players[ID].getHealth())
				progress_bars[ID].set_player_image(self.lista_players[ID].face)
				progress_bars[ID].set_player_name(self.lista_players[ID].name)
				progress_bars[ID].spawn()

			if keys[pygame.K_d] and not self.lista_players[self.ID_PLAYER].AnimStart:
				self.counter += 1
				self.lista_queue.append((Key_D(),self.counter))
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_D(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				if not self.lista_players[self.ID_PLAYER].AnimStart:
					if self.lista_players[self.ID_PLAYER].status != 0:
						self.lista_players[self.ID_PLAYER].skin_counter = 0
					self.lista_players[self.ID_PLAYER].setStatus(0)
					self.lista_players[self.ID_PLAYER].setSide(1)
					self.lista_players[self.ID_PLAYER].move_collide([20,0],[platform.getHitBox() for platform in self.lista_platforms])
					if self.lista_players[self.ID_PLAYER].hitBox.right > 1360:
						self.lista_players[self.ID_PLAYER].move_to(pygame.Vector2(0,self.lista_players[self.ID_PLAYER].y))
					elif self.lista_players[self.ID_PLAYER].hitBox.left < 0:
						self.lista_players[self.ID_PLAYER].hitBox.right = 1360
						self.lista_players[self.ID_PLAYER].move_to(pygame.Vector2(self.lista_players[self.ID_PLAYER].hitBox.x,self.lista_players[self.ID_PLAYER].y))

			if keys[pygame.K_a] and not self.lista_players[self.ID_PLAYER].AnimStart:
				self.lista_queue.append((Key_A(),self.counter))
				self.counter += 1
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_A(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				if not self.lista_players[self.ID_PLAYER].AnimStart:
					if self.lista_players[self.ID_PLAYER].status != 0:
						self.lista_players[self.ID_PLAYER].skin_counter = 0
					self.lista_players[self.ID_PLAYER].setStatus(0)
					self.lista_players[self.ID_PLAYER].setSide(0)
					self.lista_players[self.ID_PLAYER].move_collide([-20,0],[platform.getHitBox() for platform in self.lista_platforms])
					if self.lista_players[self.ID_PLAYER].hitBox.left < 0:
						self.lista_players[self.ID_PLAYER].hitBox.right = 1360
						self.lista_players[self.ID_PLAYER].move_to(pygame.Vector2(self.lista_players[self.ID_PLAYER].hitBox.x,self.lista_players[self.ID_PLAYER].y))

			if keys[pygame.K_w]:
				self.lista_queue.append((Key_W(),self.counter))
				self.counter += 1
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_W(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				self.lista_players[self.ID_PLAYER].move_collide([0,-10],[platform.getHitBox() for platform in self.lista_platforms])

			if keys[pygame.K_s]:
				self.lista_queue.append((Key_S(),self.counter))
				self.counter += 1
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_S(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				self.lista_players[self.ID_PLAYER].move_collide([0,10],[platform.getHitBox() for platform in self.lista_platforms])

			if keys[pygame.K_v]:
				self.lista_queue.append((Key_V(),self.counter))
				self.counter += 1
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_V(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				self.lista_players[self.ID_PLAYER].skin_counter = 0
				self.lista_players[self.ID_PLAYER].setStatus(4)
				self.lista_players[self.ID_PLAYER].AnimStart = True

			if keys[pygame.K_e]:
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_E(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()

			if keys[pygame.K_l]:
				#counter += 1
				#lista_queue.append((Key_L(),counter))
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_L(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				if self.lista_players[self.ID_PLAYER].fire() != None  and len(self.lista_bullet) == 0:
					if self.lista_players[self.ID_PLAYER].weapon.sound != None and self.lista_players[self.ID_PLAYER].weapon.sound.get_num_channels() == 0:
						self.lista_players[self.ID_PLAYER].weapon.sound.play()

			if keys[pygame.K_SPACE] and not self.lista_players[self.ID_PLAYER].AnimStart and not self.lista_players[self.ID_PLAYER].isJump:
				self.lista_queue.append((Key_SPACE(),self.counter))
				self.counter += 1
				self.no_key = False
				send_commands_thread = threading.Thread(target = self.send_udp , args=((Key_SPACE(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				self.lista_players[self.ID_PLAYER].move_collide([0,-220],[platform.getHitBox() for platform in self.lista_platforms])
				self.lista_players[self.ID_PLAYER].isJump = True

			if self.no_key:
				self.lista_queue.append((No_Key(),self.counter))
				self.counter += 1
				send_commands_thread = threading.Thread(target = self.send_udp , args=((No_Key(),self.counter),self.server_udp_informations,))
				send_commands_thread.start()
				if not self.lista_players[self.ID_PLAYER].AnimStart and self.lista_players[self.ID_PLAYER].getHealth() > 0:
					self.lista_players[self.ID_PLAYER].setStatus(2)

			if keys[pygame.K_ESCAPE]:
				self.lista_menus.add(MenuInGamee((int(widthScreen/2),int(HeightScreen/2)), self.win, self.z, self.server_udp_informations))

			self.lista_players[self.ID_PLAYER].playAnimation()
	
			Gravita.apply(self.lista_players[self.ID_PLAYER],self.lista_platforms)
			self.lista_players[self.ID_PLAYER].setJump([platform.getHitBox() for platform in self.lista_platforms])
			self.counter += 1
			self.lista_queue.append((Gravita,self.counter))

			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()

	def podio(self):
		widthScreen = self.win.get_rect()[2]
		HeightScreen = self.win.get_rect()[3]

		self.background = None

		next_button = ImageButton(widthScreen*0.95,80,self.image_next_button[0],Music.click)

		counter = 0

		while self.run_podio:
			self.clock.tick(40)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.allScenesFalse()
					self.run_menu = True
			
			self.win.fill(self.background_color)

			next_button.spawn()

			if next_button.clicked():
				self.allScenesFalse()
				self.run_menu = True

			self.win.blit(self.image_base,(529,597))

			if self.winner:
				Music.win.play()
				self.win_image.spawn(False)
				if counter >= self.class_players[self.index].winner.get_length():
					counter = 0
				self.win.blit(self.class_players[self.index].winner.get_item(counter),(547,229))
			else:
				Music.lose.play()
				self.loser_image.spawn(False)
				if counter >= self.class_players[self.index].loser.get_length():
					counter = 0
				self.win.blit( self.class_players[self.index].loser.get_item(counter),(547,229))

			counter += 1
			

			self.lista_menus.draw(self.win)
			self.lista_menus.update()

			pygame.display.update()