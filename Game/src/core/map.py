import pygame
from src.core.camera import camera
from math import ceil


#Classe para os blocos presentes no mapa
map_folder_location = "content/maps"
image_path = "content/images"
tile_size = 32

# Classe para o bloco do mapa
class TileKind:
    def __init__(self, name, image, is_solid): # Recebe o nome, o caminho da imagem e um booleano para saber se é ou não sólido
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid
        
        
# Classe para o mapa do jogo

class Map:
    def __init__(self, data, tile_kinds): # Recebe como parâmetros o caminho do mapa, os blocos e o tamanho dos blocos (precisam ser iguais)
        global map                        # Torna a variavel map global para ser usada em area
        
        self.tile_kinds = tile_kinds      # Coloca o tipo de bloco
        self.tile_size = tile_size        # Coloca o tamanho do bloco
        self.tiles = []                   # Lista para os blocos a serem inseridos no mapa
        for line in data.split('\n'):     # Loop para ler os blocos do mapa 
            row = []                      # Lista para percorrer a coluna da matriz que é o mapa
            for tile_number in line:      # Loop para adicionar o bloco na lista de blocos (tiles)
                row.append(int(tile_number))
            self.tiles.append(row)
        self.num_tiles_x = len(self.tiles[0])  # Número de blocos no eixo X
        self.num_tiles_y = len(self.tiles)  # Número de blocos no eixo Y
        map = self

    def draw(self, screen):
        # Desenha o mapa na tela
        for y, row in enumerate(self.tiles):                                              # Loop que percorre os blocos 
            for x, tile in enumerate(row):                                                # Percorre os blocos na linha
                location = (x * self.tile_size - camera.x, y * self.tile_size - camera.y) # desenha ele no local desejado
                image = self.tile_kinds[tile].image                                       # pega a imagem do bloco para desenhar
                screen.blit(image, location)                                              # coloca na tela
            
            

    # Função para definir se o bloco é sólido ou não
    def is_point_solid(self, x, y):                    # Parametros = x e y que são posições
        x_tile = int(x/self.tile_size)                 # Pega a razão da posição e do tamanho do bloco para checar se haverá colisão
        y_tile = int(y/self.tile_size)                
        if x_tile < 0 or \
            y_tile < 0 or \
                y_tile >= len(self.tiles) or \
                    x_tile >= len(self.tiles[y_tile]): # Se a razão for 0 (ta por cima) ou maior ou igual que o tamanho de um bloco retorna falso
                        return False
        tile = self.tiles[y_tile][x_tile]              # Cria a variavel para receber o bloco que receberá a característica
        return self.tile_kinds[tile].is_solid          # Retorna ao bloco se é sólido
    
    def is_rect_solid(self, x, y, width, height):      # Função para detectar a colisão do objeto, parametros = posição e dimensões de um objeto
        x_checks = int (ceil(width/self.tile_size))    # Pega a razão entre as dimensões com o tamanho do objeto
        y_checks = int (ceil(height/self.tile_size))
        for yi in range (y_checks):                    # Loop que checa se o bloco é sólido e se o objeto está encostando nele
            for xi in range(x_checks):
                x = xi * self.tile_size + x
                y = yi * self.tile_size + y
                if self.is_point_solid(x,y):
                    return True                        # Retorna True (colisão)
        # Checagem de colisões para Retornar True (não passa ali) ou False (passa por cima)
        if self.is_point_solid(x + width, y): 
            return True
        if self.is_point_solid(x, y + height):
            return True
        if self.is_point_solid(x+ width, y + height):
            return True
        return False

# Classe da chave que é a condição de vitória do jogo
class Key:
    def __init__(self, x, y, image): # Ela tem como parâmetros sua posição e uma imagem
        self.x = x
        self.y = y
        self.image = image
        self.collected = False  # Condição se ela é ou não desenhada, se false ela está no mapa, se true ela foi pega

    def get_rect(self): # Função para retornar um retangulo da chave para detectar a colisão
        #Retorna um retângulo para facilitar a detecção de colisão
        return pygame.Rect(self.x , self.y , self.image.get_width(), self.image.get_height())

    def draw(self, screen, camera): # Função de desenhar a chave
        if not self.collected:      # só desenhamos se ela não for coletada
            screen.blit(self.image, (self.x - camera.x, self.y - camera.y))




