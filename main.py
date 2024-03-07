from pygame import *
from math import *

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
BLUISH_GREY = (86, 100, 135, 53)
LASER_YELLOW = (255, 231, 0, 100)
#----------------------------

#Funciones

#----------------------------

#Clases
class GameEntity(sprite.Sprite):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__()
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.scale(self.image, (self.sizeX, self.sizeY))
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.vida = vida

class Player(GameEntity):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__(sprite, posX, posY, sizeX, sizeY, vida)
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.mouse_pos = 0

    def update(self, sprite, mouse_pos):
        self.velocityX = 0
        self.velocityY = 0
        self.mouse_pos = mouse_pos

        teclas = key.get_pressed()

        #Movimiento con WASD
        if teclas[K_w]:
            self.velocityY = -12.5
        if teclas[K_s]:
            self.velocityY = 12.5
        if teclas[K_a]:
            self.velocityX = -12.5
        if teclas[K_d]:
            self.velocityX = 12.5

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        #Rotacion del personaje hacia el mouse
        self.angle = degrees(atan2((self.mouse_pos[1] - self.rect.centery), (self.mouse_pos[0] - self.rect.centerx))) + 90
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.rotate(self.image, - self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        #Calcular distancia en X entre el player y el mouse
        #mouse_pos[0] - self.rect.centerx 

        #Calcular distancia en Y entre el player y el mouse
        #mouse_pos[1] - self.rect.centery

        #Calcular distancia entre el player y el mouse
        #sqrt(((mouse_pos[0] - self.rect.centerx) ** 2) + ((mouse_pos[1] - self.rect.centery) ** 2))

        #Calcular el ángulo entre el player, y el mouse
        #degrees(atan2((mouse_pos[1] - self.rect.centery), (mouse_pos[0] - self.rect.centerx)))


        #Limitar el movimiento del player en la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_size[1]:
            self.rect.bottom = screen_size[1]

        #Funcion para disparar la o las balas del player
        #Se ejecuta exclusivamente en el for de los eventos en el loop principal
    def Shoot(self, event, objects):

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            objects.add(Bullet(self.rect.center, self.angle))

class Bullet(sprite.Sprite):
    def __init__(self, location, angle):
        super().__init__()
        self.image = image.load("Assets/laser_beam.png").convert_alpha()
        self.image = transform.scale(self.image, (20, 20))
        #Rota la bala hacia donde está viendo el player
        self.angle = radians(angle - 90)
        self.image = transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center = location)
        self.move = [self.rect.x, self.rect.y]
        #Se calcula la velocidad en X y en Y respectivamente
        self.speed_magnitude = 20
        self.speed = (self.speed_magnitude* cos(self.angle),
                      self.speed_magnitude* sin(self.angle))
        
    def update(self, screen_rect):
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move
        self.remove(screen_rect)

    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()
#----------------------------

#Variables
player_sprite = "Assets/tiny_ship14.png"
#----------------------------

#Objetos
All_sprite_in_game = sprite.Group()
player = Player(player_sprite, 500, 500, 40, 40, 10)
#----------------------------

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        #Para que funcione el disparo
        player.Shoot(e, All_sprite_in_game)

    screen.fill(DARK_BLUE)

    #Logica principal del juego

    screen_rect = display.get_surface().get_rect()

    #Posicion del mouse
    mouse_pos = mouse.get_pos()

    player.update(player_sprite, mouse_pos)
    screen.blit(player.image, player.rect)
    All_sprite_in_game.update(screen_rect)
    #-----------------

    #Configuración de la pantalla (In-Game)
    All_sprite_in_game.draw(screen)
    display.flip()
        #Control de los fps o cuadros por segundo
    clock.tick(60)
    #-----------------

quit()