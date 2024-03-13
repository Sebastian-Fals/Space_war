from pygame import *
from math import *
import time as tm

#Se importan las clases y demás
from GameEntities import Player, Enemies
from funciones import get_image, responsiveSizeAndPosition

#Se inicia el programa
init()

#Configuración de la pantalla
resolucion = (1920, 1080)
screen = display.set_mode(resolucion, FULLSCREEN)
clock = time.Clock()
#----------------------------

text_font = font.Font("PixelifySans-VariableFont_wght.ttf", 30)

#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35, 14)
#----------------------------
#Grupos
bullets = sprite.Group()
enemies = sprite.Group()
#----------------------------
#Sprite sheets
playerSheet = image.load("Assets/SpaceShip_sheet.png").convert_alpha()
bulletsSheet = image.load("Assets/Bullets_sheet.png").convert_alpha()
#----------------------------

#Objetos
player = Player(get_image(playerSheet, 0, 52, 52, BLACK), get_image(bulletsSheet, 0, 24, 24, BLACK), (500, 500), (40, 40), 10)
enemie = Enemies(image.load("Assets/circular_enemy.png").convert_alpha(), get_image(bulletsSheet, 1, 24, 24, BLACK), (300, 300), (40, 40), 10, "enemigo_patron_circular")
enemies.add(enemie)
#----------------------------

last_time = tm.time()#Esta variabe sirve para calcular el deltaTime

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:

    #Tamaño de la pantalla
    screen_size = screen.get_size()

    #Fonts
    fps_font = font.Font("PixelifySans-VariableFont_wght.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2)))

    #DeltaTime
    dt = tm.time() - last_time
    dt *= 60
    last_time = tm.time()

    #Dibuja el fondo
    screen.fill(DARK_BLUE)

    #Muestra los fps
    fps = clock.get_fps()
    fps_text = fps_font.render("FPS: " + str(int(fps//1)), False, WHITE)
    screen.blit(fps_text, (responsiveSizeAndPosition(screen_size, 0, 96), responsiveSizeAndPosition(screen_size, 1, 1)))

    #Event manager
    for e in event.get():
        if e.type == QUIT:
            running = False
        #Para que funcione el disparo
        player.Shoot(e, bullets)

    #Logica principal del juego

    screen_rect = display.get_surface().get_rect()

        #Posicion del mouse
    mouse_pos = mouse.get_pos()

        #Logica de las colisiones
    bullets_to_enemies = sprite.groupcollide(enemies, bullets, False, False)

    for enemy, bullet in bullets_to_enemies.items():
        for b in bullet:
            if b.bullet_target == "enemies":
                enemy.take_damage(1)
                b.kill()

        #Update de los objetos de la escena
    player.update(dt, mouse_pos, screen_size)
    enemies.update(bullets)
    bullets.update(screen_rect, dt)
    #-----------------

    #Configuración de la pantalla (In-Game)
    screen.blit(player.image, player.rect) #Se dibuja el player en pantalla
    bullets.draw(screen)
    enemies.draw(screen)
    display.flip()

    clock.tick(60)#Control de los fps o cuadros por segundo
    #-----------------

quit()