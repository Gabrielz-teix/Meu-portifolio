import pygame
import math

# Classe responsável pela lanterna, aqui criamos uma tela escura por cima do mapa e um cone de luz para ser a area iluminada pela lanterna
class Lanterna:
    def __init__(self, raio, angulo, escurecimento=(0, 0, 0, 150), cor_luz=(255, 255, 255, 50)): 
    
        #Inicializa a lanterna.
        # parametro raio: Raio máximo de alcance da luz.
        # parametro angulo: Ângulo do cone de luz em graus.
        # parametro escurecimento: Cor e opacidade da camada escurecida.
        # parametro cor_luz: Cor e opacidade do cone de luz.
        
        self.raio = raio
        self.angulo = angulo
        self.escurecimento = escurecimento
        self.cor_luz = cor_luz
        self.ligada = False
        self.lanterna_pos_y = 0
        self.lanterna_pos_x = 0

    def desenhar(self, screen, player_x, player_y, player_width, player_height, camera_x, camera_y):
        
        #Desenha a lanterna sobre a tela.
        #parametro screen: Tela do jogo.
        #parametro player_x: Posição X do jogador.
        #parametro player_y: Posição Y do jogador.
        #parametro player_width: Largura do jogador.
        #parametro player_height: Altura do jogador.
        #parametro camera_x: Posição X da câmera.
        #parametro camera_y: Posição Y da câmera.
     
        # Cria a camada de escurecimento
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(self.escurecimento)

        # Calcula a posição da lanterna ajustada pela câmera
        keys = pygame.key.get_pressed()
        
        self.lanterna_pos_x = player_x + player_width // 2 - camera_x + 30
        self.lanterna_pos_y = player_y + player_height // 2 - camera_y + 30

        if self.ligada:
            # Direção da luz (baseada na posição do mouse)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dir_x, dir_y = mouse_x - self.lanterna_pos_x, mouse_y - self.lanterna_pos_y
            angle = math.atan2(dir_y, dir_x)

            # Cria os pontos do cone de luz
            points = [(self.lanterna_pos_x, self.lanterna_pos_y)]
            for i in range(-self.angulo // 2, self.angulo // 2 + 1, 5):
                end_x = self.lanterna_pos_x + int(self.raio * math.cos(angle + math.radians(i)))
                end_y = self.lanterna_pos_y + int(self.raio * math.sin(angle + math.radians(i)))
                points.append((end_x, end_y))

            # Desenha o cone de luz
            pygame.draw.polygon(overlay, self.cor_luz, points)

        # Aplica o overlay à tela
        screen.blit(overlay, (0, 0))
