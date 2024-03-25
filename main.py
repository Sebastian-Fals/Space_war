from pygame import *
from math import *
import sys
import time as tm

#Se importan las clases y demás
from GameEntities import Player
from funciones import get_image, responsiveSizeAndPosition, AAfilledRoundedRect
from EnemyGenerator import EnemyGenerator, SpawnPoint

#Se inicia el programa
init()

#Configuración de la pantalla
monitor_size = [display.Info().current_w, display.Info().current_h]
resolucion = (1280, 720)
screen = display.set_caption("Space war")
screen = display.set_mode(resolucion, DOUBLEBUF, 32)
screen_size = screen.get_size()
clock = time.Clock()
#----------------------------

#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35, 14)
#----------------------------

#Logica de los niveles o pantallas
click = False
#----------------------------

#Pantallas
def mainMenu():
    while True:
        screen.fill(DARK_BLUE)

        #Mouse position
        mx, my = mouse.get_pos()

        #Title
        mainMenuFont = font.Font("Assets/Vermin_Vibes_1989.ttf", int(responsiveSizeAndPosition(screen_size, 1, 15)))
        mainMenuText = mainMenuFont.render("SPACE WAR", True, WHITE)
        mainMenuShadowText = mainMenuFont.render("SPACE WAR", True, (76, 117, 117))
        screen.blit(mainMenuShadowText, mainMenuShadowText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50.7), responsiveSizeAndPosition(screen_size, 1, 30.7))))
        screen.blit(mainMenuText, mainMenuText.get_rect(center= (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 30))))

        #Boton Play
        buttonPlayFont = font.Font("Assets/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 5)))
        buttonPlayText = buttonPlayFont.render("PLAY", True, WHITE)
        if buttonPlayText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 50))).collidepoint((mx, my)):
            buttonPlayText = buttonPlayFont.render("PLAY", True, (154, 237, 237))
            if click:
                Game()

        #Event manager
        click = False
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
                    print(click)

        #Pintar el boton play en la pantalla
        screen.blit(buttonPlayText, buttonPlayText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 50))))

        display.flip()
        clock.tick(60)

def Game():
    screen_size = screen.get_size()

    #Grupos
    bullets = sprite.Group()
    enemies = sprite.Group()
    playerGroup = sprite.Group()
    #----------------------------
    #Sprite sheets
    playerSheet = image.load("Assets/SpaceShip_sheet.png").convert_alpha()
    bulletsSheet = image.load("Assets/Bullets_sheet.png").convert_alpha()
    #----------------------------

    #Se guardan todas las balas en un array
    bullet_array = [get_image(bulletsSheet, 0, 24, 24, BLACK),
                    get_image(bulletsSheet, 1, 24, 24, BLACK),
                    get_image(bulletsSheet, 2, 24, 24, BLACK)]

    #Posibles posiciones de un enemigo
    enemyPos = [SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 25), responsiveSizeAndPosition(screen_size, 1, 10))), 
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 75), responsiveSizeAndPosition(screen_size, 1, 10))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 25), responsiveSizeAndPosition(screen_size, 1, 90))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 75), responsiveSizeAndPosition(screen_size, 1, 90))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 20))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 80))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 10), responsiveSizeAndPosition(screen_size, 1, 50))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 90), responsiveSizeAndPosition(screen_size, 1, 50)))]

    enemyID = ["enemigo_patron_circular", 
            "enemigo_patron_espiral"]

    #Objetos
    player = Player(get_image(playerSheet, 0, 52, 52, BLACK), bullet_array[0], (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 90)), (responsiveSizeAndPosition(screen_size, 0, 3), responsiveSizeAndPosition(screen_size, 0, 3)), 10)
    playerGroup.add(player)
    enemyGenerator = EnemyGenerator(enemies, enemyPos, 0, enemyID, bullet_array, "easy", screen, screen_size)
    #----------------------------
    last_time = tm.time()#Esta variabe sirve para calcular el deltaTime
    running = True
    while running:

        #Tamaño de la pantalla
        screen_size = screen.get_size()

        #Fonts
        fps_font = font.Font("Assets/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))

        #DeltaTime
        dt = tm.time() - last_time
        dt *= 60
        last_time = tm.time()

        #Dibuja el fondo
        screen.fill(DARK_BLUE)

        #Muestra los fps
        fps = clock.get_fps()
        fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
        screen.blit(fps_text, fps_text.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 97), responsiveSizeAndPosition(screen_size, 0, 1))))

        #Event manager
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_f:
                    enemyGenerator.generateEnemy()
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

        bullet_to_player = sprite.groupcollide(playerGroup, bullets, False, False)
        for player, bullet in bullet_to_player.items():
            for b in bullet:
                if b.bullet_target == "player":
                    player.take_damage(1)
                    b.kill()
        #Si mueres te devuelve al menu principal
        if player.isDead:
            running = False

            #Update de los objetos de la escena
        for position in enemyPos:
            position.update(enemies)           
        playerGroup.update(dt, mouse_pos, screen_size)
        enemies.update(bullets)
        enemyGenerator.update()
        bullets.update(screen_rect, dt)
        #-----------------

        #Configuración de la pantalla (In-Game)
        playerGroup.draw(screen) #Se dibuja el player en pantalla
        bullets.draw(screen)
        enemies.draw(screen)
        display.flip()

        clock.tick(60)#Control de los fps o cuadros por segundo
        #-----------------
#----------------------------

mainMenu()

quit()
sys.exit()