import pygame
from src.core.camera import camera

sprites = []  # Sprites ativas no jogo
loaded = {}  # Sprites já carregadas para evitar duplicação

# Classe de Sprite
class Sprite:
    def __init__(self, image):                    # Inicia com o arquivo de imagem
        if image in loaded:                       # Se já estiver no dicionário loaded
            self.image = loaded[image]            # Não caregamos 
        else:
            self.image = pygame.image.load(image) # Se não, nós carregamos ela
            loaded[image] = self.image            # adicionamos em loaded

        sprites.append(self)                      # Adicionamos na lista de sprites ativas

    def delete(self): 
        #Remove a sprite da lista de sprites ativas
        sprites.remove(self)

    def draw(self, screen):
        #Desenha a sprite na posição atual
        screen.blit(self.image, (self.entity.x - camera.x, self.entity.y - camera.y))
