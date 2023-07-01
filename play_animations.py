import threading
import time

def play(win,x,y,lista_sprites,play_animation,clock):
    clock.tick(20)
    if not play_animation:
        for sprite in lista_sprites:
            win.blit(sprite,(x,y))

def animations(win,x,y,lista_sprites,play_animation,clock):
    t = threading.Thread(target = play , name= 'tar1' , args=(win,x,y,lista_sprites,play_animation,clock))
    t.start()
 





