from pygame import *
from math import *

#Se importan las clases y demás
from GameEntities import Player, Enemies

#Se inicia el programa
init()

#Configuración de la pantalla
resolucion = (1920, 1080)
screen = display.set_mode(resolucion, FULLSCREEN)
clock = time.Clock()
screen_size = screen.get_size()
#----------------------------

#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35, 14)
#----------------------------
#Grupos
bullets = sprite.Group()
enemies = sprite.Group()
#----------------------------
#Variables
player_sprite = "Assets/tiny_ship14.png"
bullet_sprites = "Assets/laser_beam.png"
#----------------------------

#Objetos
player = Player(player_sprite, bullet_sprites, 500, 500, 40, 40, 10)
enemie = Enemies("Assets/circular_enemy.png", bullet_sprites, 300, 300, 40, 40, 10, "enemigo_patron_circular")
enemies.add(enemie)
#----------------------------

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        #Para que funcione el disparo
        player.Shoot(e, bullets)

    screen.fill(DARK_BLUE)

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
    player.update(player_sprite, mouse_pos, screen_size)
    enemies.update(bullets)
    bullets.update(screen_rect)
    #-----------------

    #Configuración de la pantalla (In-Game)
    screen.blit(player.image, player.rect) #Se dibuja el player en pantalla
    bullets.draw(screen)
    enemies.draw(screen)
    display.flip()

    clock.tick(60)#Control de los fps o cuadros por segundo
    #-----------------

quit()