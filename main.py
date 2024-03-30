from pygame import *
from math import *
from random import *
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
    stars = []
    for _ in range(500):
            randomWhite = randint(150, 230)
            randSize = randint(1, 3)
            randSpeed = randint(1, 10)
            particleRect = Rect(randint(0, screen_size[0]), randint(0, screen_size[1]), randSize, randSize)
            stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])

    click = False
    bg_music = mixer.music
    bg_music.load("Assets/SkyFire_(Title Screen).ogg")
    bg_music.play(-1)
    bg_music.set_volume(0.4)

    button = mixer.Sound("Assets/click.mp3")
    button.set_volume(0.3)
    while True:
        #Se dibuja el fondo
        screen.fill(BLACK)
        for particle in stars:
            particle[1][1] += particle[3]
            if particle[1][1] > screen_size[1]:
                particle[3] = randint(1, 10)
                particle[1][1] = 0
            draw.circle(screen, particle[0], particle[1], particle[2])

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
                bg_music.pause()
                button.play()
                tm.sleep(0.3)
                Game(stars)
                bg_music.load("Assets/SkyFire_(Title Screen).ogg")
                bg_music.play(-1)
                bg_music.set_volume(0.2)


        #Event manager
        click = False
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

        #Pintar el boton play en la pantalla
        screen.blit(buttonPlayText, buttonPlayText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 50))))

        display.flip()
        clock.tick(60)

def Game(stars):
    screen_size = screen.get_size()

    #Musica de fondo
    bg_game_music  = mixer.music
    bg_game_music.load("Assets/Rain_of_Lasers.ogg")
    bg_game_music.play(-1)
    bg_game_music.set_volume(0.2)
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
                    get_image(bulletsSheet, 2, 24, 24, BLACK),
                    get_image(bulletsSheet, 3, 24, 24, BLACK),
                    get_image(bulletsSheet, 4, 24, 24, BLACK),
                    get_image(bulletsSheet, 5, 24, 24, BLACK),
                    get_image(bulletsSheet, 6, 24, 24, BLACK)]

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
            "enemigo_patron_espiral",
            "enemigo_patron_espiral_alternado", 
            "enemigo_patron_circular_alternado",
            "enemigo_patron_estrella",
            "enemigo_patron_spray"]

    #Objetos
    player = Player(get_image(playerSheet, 0, 52, 52, BLACK), bullet_array[0], (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 90)), (responsiveSizeAndPosition(screen_size, 0, 3), responsiveSizeAndPosition(screen_size, 0, 3)), 10)
    playerCollide = Rect(player.rect.x, player.rect.y, responsiveSizeAndPosition(screen_size, 0, 0.5), responsiveSizeAndPosition(screen_size, 0, 0.5))
    playerGroup.add(player)
    enemyGenerator = EnemyGenerator(enemies, enemyPos, 0, enemyID, bullet_array, "easy", screen, screen_size)
    coins = 0
    #----------------------------
    last_time = tm.time()#Esta variabe sirve para calcular el deltaTime
    running = True
    while running:

        #Tamaño de la pantalla
        screen_size = screen.get_size()

        playerCollide.center = player.rect.center

        #Fonts
        fps_font = font.Font("Assets/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))

        #DeltaTime
        dt = tm.time() - last_time
        dt *= 60
        last_time = tm.time()

        #Dibuja el fondo
        screen.fill(BLACK)
        for particle in stars:
            particle[1][1] += particle[3]
            if particle[1][1] > screen_size[1]:
                particle[3] = randint(1, 10)
                particle[1][1] = 0
            draw.circle(screen, particle[0], particle[1], particle[2])


        #Muestra los fps
        fps = clock.get_fps()
        fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
        screen.blit(fps_text, fps_text.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 97), responsiveSizeAndPosition(screen_size, 0, 1))))

        #Muestra el puntaje
        coins_font = font.Font("Assets/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 3)))
        coins_text = coins_font.render("Score: " + str(coins), True, WHITE)
        screen.blit(coins_text, (responsiveSizeAndPosition(screen_size, 0 , 2), responsiveSizeAndPosition(screen_size, 1, 2)))

        #Event manager
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_f:
                    enemyGenerator.generateEnemy()
                if e.key == K_ESCAPE:
                    quit()
                    sys.exit()
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

        for bullet in bullets:
            if bullet.bullet_target == "player" and playerCollide.colliderect(bullet.rect):
                player.take_damage(1)
                bullet.kill()
        #Si mueres te devuelve al menu principal
        if player.isDead:
            bg_game_music.unload()
            running = False

            #Update de los objetos de la escena
        for position in enemyPos:
            position.update(enemies)           
        playerGroup.update(dt, mouse_pos, screen_size)
        for enemy in enemies:
            if enemy.vida == 0:
                coins += 1
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