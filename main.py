from pygame import *

#Se inicia el programa
init()

screen = display.set_mode((1920, 1080), FULLSCREEN)
clock = time.Clock()
running = True

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill("purple")

    display.flip()
    
    clock.tick(60)

quit()
