import pygame
from Jogo.src.components.physics import Body
from Jogo.src.components.entity import active_objs, Entity
from Jogo.src.core.input import is_key_pressed
from Jogo.src.core.camera import camera
from Jogo.src.components.label import Label
import math
from Jogo.src.core.sons import som_passo


# Velocidade de movimento do jogador
MOVEMENT_SPEED = 15

# Classe que representa o jogador
class Player:
    def __init__(self):
        active_objs.append(self)                                # Adiciona Player a lista de objetos 
        self.sprite_size = 32                                   # Tamanho da Sprite
        self.scale_factor = 2                                   # Multiplicador de tamanho do player
        self.frame_index = 0                                    # Contador de indice de frame 
        self.direcao = "down"                                   # Direção inicial que o jogador está apontado
        self.current_frames = []                                # Lista para armazenar os Sprites
        self.load_sprites("Jogo/content/images/spritesheet.png")  # Spritesheet carregado
        self.current_frames = self.idle_frames                  # Começa parado
        
        # Cria um texto no mapa
        self.area_label = Entity(Label("main/EBGaramond-Regular.ttf", "Encontre a chave da cabana e retorne")).get(Label)
        self.loc_label = Entity(Label("main/EBGaramond-Regular.ttf", "X: 0 - Y: 0")).get(Label)
        
        self.loc_label.entity.y = camera.height - 50
        self.loc_label.entity.x = 10
        self.area_label.entity.x = 10 # Define a posição do texto

    # Função de carregar o Spritesheet
    def load_sprites(self, spritesheet_path):
        """Carrega e divide o spritesheet."""
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha() # Carrega o Spritesheet
        rows = 6                                                          # 6 Linhas (6 ações)
        cols = 4                                                          # 4 Colunas (4 estados para cada ação)
        frames = []                                                       # Lista para armazenar os frames

        for row in range(rows):                                           # Loop para percorrer as linhas
            for col in range(cols):                                       # Loop para percorrer as colunas
                x = col * self.sprite_size                                # Posição de cada estado do spritesheet
                y = row * self.sprite_size
                frame = spritesheet.subsurface((x, y, self.sprite_size, self.sprite_size))  # Carrega o frame
                frame = pygame.transform.scale(frame, (self.sprite_size * self.scale_factor, self.sprite_size * self.scale_factor)) # Passa ele pro Jogador
                frames.append(frame) # Adiciona na lista de frames

        self.idle_frames = frames[0:4]          # Frame Parado
        self.walk_down_frames = frames[4:8]     # Frame andando para baixo
        self.walk_left_frames = frames[8:12]    # Frame andando para esquerda
        self.walk_right_frames = frames[12:16]  # Frame andando para direita
        self.idle_back_frames = frames[16:20]   # Frame andando para baixo
        self.walk_up_frames = frames[20:24]     # Frame andando para cima

    def update(self): # Função para atualizar o Jogador
        self.loc_label.set_text(f"X: {self.entity.x} - Y: {self.entity.y}")
        previous_x = self.entity.x # Guarda a posição anterior do jogador caso ele não consiga passar em algum lugar
        previous_y = self.entity.y
        body = self.entity.get(Body) # Cria o corpo do jogador para física
        
        moving = False  # Variável para rastrear se o jogador está se movendo
        
        # Checa qual tecla está sendo pressionada e retorna a animação e atualiza a direção que ele está olhando
        if is_key_pressed(pygame.K_w):
            self.entity.y -= MOVEMENT_SPEED
            self.current_frames = self.walk_up_frames 
            self.direcao = -math.pi / 2  # -90° (para cima)
            moving = True
        elif is_key_pressed(pygame.K_s):
            self.entity.y += MOVEMENT_SPEED
            self.current_frames = self.walk_down_frames
            self.direcao = math.pi / 2  # 90° (para baixo)
            moving = True
        elif is_key_pressed(pygame.K_a):
            self.entity.x -= MOVEMENT_SPEED
            self.current_frames = self.walk_left_frames
            self.direcao = math.pi  # 180° (para a esquerda)
            moving = True
        elif is_key_pressed(pygame.K_d):
            self.entity.x += MOVEMENT_SPEED
            self.current_frames = self.walk_right_frames
            self.direcao = 0  # 0 radianos (para a direita)
            moving = True
        else:
            self.current_frames = self.idle_frames
        
        # Se o jogador estiver se movendo e o som não estiver tocando, inicie o som
        if moving:
            if som_passo.get_num_channels() == 0:  # Verifica se o som já está tocando
                som_passo.set_volume(0.1)  # Ajuste o volume conforme necessário
                som_passo.play(loops=-1)  # -1 faz o som repetir indefinidamente
        else:
            som_passo.stop()  # Para o som quando o jogador parar de se mover

        # Se a posição que o corpo vai assumir não for válida (tem um objeto no caminho) ele fica na posição
        if not body.is_position_valid():
            self.entity.y = previous_y
        if not body.is_position_valid():
            self.entity.x = previous_x

        # Vai trocando os frames
        self.frame_index = (self.frame_index + 1) % len(self.current_frames)

        # Atualiza a posição da câmera
        camera.x = self.entity.get_rect().centerx - camera.width / 2
        camera.y = self.entity.get_rect().centery - camera.height / 2

    def draw(self, screen):
        """Desenha o personagem na tela."""
        screen.blit(self.current_frames[self.frame_index], (self.entity.x - camera.x, self.entity.y - camera.y))
