import pygame
import math
from Jogo.src.components.entity import active_objs
from Jogo.src.core.camera import camera  
from Jogo.src.components.physics import Body  
from Jogo.src.components.entity import Entity
from Jogo.src.core.lanterna import Lanterna
from Jogo.src.core.sons import som_fantasma, som_fantasma_perto


# Configurações da lanterna
lanterna = Lanterna(raio=200, angulo=60, escurecimento=(0, 0, 0, 150)) 

# Classe Enemy responsável pelo fantasma
class Enemy:
    def __init__(self, player): # Recebe os parametros do player pois segue a mesma linha de desenho e lógica
        active_objs.append(self)
        self.player = player  
        self.x = 32 * 90
        self.y = 32 * 55
        self.speed = 5
        self.sprite_size = 32
        self.scale_factor = 2
        self.frame_index = 0
        self.current_frames = []
        self.direction = "down"
        self.animation_timer = 10
        self.animation_speed = 1

        self.load_sprites("Jogo/content/images/enemy_spritesheet.png")
        self.current_frames = self.walk_down_frames  

    def load_sprites(self, spritesheet_path):
        """Carrega e divide o spritesheet."""
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        rows = 6
        cols = 4
        frames = []

        for row in range(rows):
            for col in range(cols):
                x = col * self.sprite_size
                y = row * self.sprite_size
                frame = spritesheet.subsurface((x, y, self.sprite_size, self.sprite_size))
                frame = pygame.transform.scale(frame, (self.sprite_size * self.scale_factor, self.sprite_size * self.scale_factor))
                frames.append(frame)

        self.idle_frames = frames[0:4]
        self.walk_down_frames = frames[4:8]
        self.walk_left_frames = frames[8:12]
        self.walk_right_frames = frames[12:16]
        self.walk_up_frames = frames[20:24]

    def update(self):
        """Movimenta o inimigo em direção ao jogador e anima corretamente."""
        player_body = self.player.get(Body) if isinstance(self.player, Entity) else None  
        if not player_body:
            print("Erro: 'player' não tem componente Body!")
            return
        
        player_x = player_body.entity.x
        player_y = player_body.entity.y
        
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy)  # Calcula a distância entre o inimigo e o jogador

        if dist != 0:
            dx /= dist
            dy /= dist

        self.x += dx * self.speed
        self.y += dy * self.speed

        if dist <= 800:  # Se o fantasma estiver perto, toca o som
            if som_fantasma_perto.get_num_channels() == 0:  # Verifica se já está tocando
                som_fantasma_perto.set_volume(0.3)  # Ajuste o volume conforme necessário
                som_fantasma_perto.play(loops=-1)  # -1 faz o som repetir indefinidamente
        else:  # Se o fantasma estiver longe, para o som
            som_fantasma_perto.stop()

        # Determina a direção do fantasma
        if abs(dx) > abs(dy):  
            if dx > 0:
                self.current_frames = self.walk_right_frames
            else:
                self.current_frames = self.walk_left_frames
        else:  
            if dy > 0:
                self.current_frames = self.walk_down_frames
            else:
                self.current_frames = self.walk_up_frames
        
        # Atualiza a animação a cada X frames
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)

    def draw(self, screen):
        """Desenha o inimigo na tela."""
        screen.blit(self.current_frames[self.frame_index], (self.x - camera.x, self.y - camera.y))
        som_fantasma_perto.stop()
        som_fantasma.set_volume(0.5) 
        som_fantasma.play(loops=0)  
        
