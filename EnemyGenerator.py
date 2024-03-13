from pygame import *
from random import *
from GameEntities import Enemies

class SpawnPoint():
    def __init__(self, position):
        self.position = position
        self.canSpawn = True

    def update(self, group):
        # Por defecto, permitir el spawn si el grupo está vacío
        self.canSpawn = True if not group.sprites() else False

        # Verificar si algún sprite en el grupo ocupa la misma posición
        for enemy in group:
            if enemy.position == self.position:
                self.canSpawn = False
                break  # Si encontramos un sprite en la misma posición, no necesitamos continuar verificando
            else:
                self.canSpawn = True
        

class EnemyGenerator():
    def __init__(self, group,  spawnPoints, enemyCount, enemies_ID, bulletSprite):
        self.spawnPionts = spawnPoints
        self.enemyCount = enemyCount
        self.enemies_ID = enemies_ID
        self.bulletSprite = bulletSprite
        self.group = group
    def update(self):
        pass

    def generateEnemy(self):
        #Verifica si todos los spawnPoints están ocupados
        all_spawn_points_occupied = all(not spawn_point.canSpawn for spawn_point in self.spawnPionts)
        if all_spawn_points_occupied:
            print("Todos los puntos de aparición están ocupados. No se puede generar un enemigo.")
            return

        randomPosition = randint(0, (len(self.spawnPionts) - 1))
        print(randomPosition)
        while self.spawnPionts[randomPosition].canSpawn == False:
            randomPosition = randint(0, (len(self.spawnPionts) - 1))
        if self.spawnPionts[randomPosition].canSpawn == True:
            self.group.add(Enemies(image.load("Assets/circular_enemy.png").convert_alpha(), self.bulletSprite, self.spawnPionts[randomPosition].position, (40, 40), 10, "enemigo_patron_circular"))
            print("Se genero un enemigo")
            print(randomPosition)