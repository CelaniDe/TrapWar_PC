from player import *
import pygame
import pickle



pygame.init()
win = pygame.display.set_mode((500,500))

run = True

clock = pygame.time.Clock()

sfera = SocialBoom()

pickled_sfera = pickle.dumps(sfera)

print(len(pickled_sfera))

sfera = pickle.loads(pickled_sfera)

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    win.fill((255,100,20))

    try:
        sfera.spawn(win)
    except Exception as e:
        print(e)

    sfera.setStatus(2)

    if keys[pygame.K_d]:
        sfera.setStatus(0)
        sfera.setSide(1)
        sfera.move()
        sfera.x += 5

    if keys[pygame.K_a]:
        sfera.setStatus(0)
        sfera.setSide(0)
        sfera.move()
        sfera.x += -5

    sfera.idle()


    pygame.display.update()

pygame.quit()