import pygame
from game import *

game = Game("TrapWar",(1360,768),120)

game.load()

while game.run_game:
    if game.run_menu:
        game.menu()
    if game.run_options:
        game.options()
    if game.run_show_keys:
        game.show_keys()
    if game.run_select_mode:
        game.select_mode()
    if game.run_menu_select_player:
        game.select_player()
    if game.run_menu_connect_to_server:
        game.connect_to_server()
    if game.wait_players:
        game.wait_players_to_play()
    if game.run_gameplay:
        game.play()
    if game.run_podio:
        game.podio()