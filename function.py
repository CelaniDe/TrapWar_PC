import pygame
import os

def ricevi_foto(nome_percorso):
    lista_pygame_foto = []
    old_directory = os.getcwd()
    os.chdir(os.getcwd()+str(nome_percorso))
    nomi_foto = os.listdir()
    nomi_foto = sorted(nomi_foto)
    for name_foto in nomi_foto:
        if "png" in name_foto or "celani" in name_foto:
            lista_pygame_foto.append(pygame.image.load(name_foto)) 
    os.chdir(old_directory)
    return lista_pygame_foto