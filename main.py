from pygame import *
from math import * 

#Se inicia el programa
init()

#Configuración de la pantalla
screen = display.set_mode((1920, 1080), FULLSCREEN)
clock = time.Clock()
screen_size = screen.get_size()
#----------------------------

#Colores
DARK_BLUE = (0, 1, 35, 14)
BLUISH_GREY = (86, 100, 135, 53)
#----------------------------

#Funciones
def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)
#----------------------------

#Clases
class GameEntity(sprite.Sprite):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__()
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.scale(self.image, (sizeX, sizeY))
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.vida = vida

class Player(GameEntity):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__(sprite, posX, posY, sizeX, sizeY, vida)
        self.velocityX = 0
        self.velocityY = 0

    def update(self):
        self.velocityX = 0
        self.velocityY = 0

        teclas = key.get_pressed()

        #Movimiento con WASD
        if teclas[K_w]:
            self.velocityY = -25
        if teclas[K_s]:
            self.velocityY = 25
        if teclas[K_a]:
            self.velocityX = -25
        if teclas[K_d]:
            self.velocityX = 25

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        #Limites en la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_size[1]:
            self.rect.bottom = screen_size[1]
#----------------------------

#Variables
player_sprite = "Assets/tiny_ship14.png"
#----------------------------

#Objetos
All_sprite_in_game = sprite.Group()
player = Player(player_sprite, 500, 500, 40, 40, 10)
All_sprite_in_game.add(player)
#----------------------------

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill(DARK_BLUE)

    #Logica principal del juego
    All_sprite_in_game.update() 
    #-----------------

    #Configuración de la pantalla (In-Game)
    All_sprite_in_game.draw(screen)
    display.flip()
        #Control de los fps o cuadros por segundo
    clock.tick(60)
    #-----------------

quit()