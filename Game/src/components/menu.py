import pygame
import time
import random

background = pygame.image.load("content/images/menu_background.jpg")

# Classe do menu do jogo
class Menu:
    def __init__(self, screen):                                              # Recebe a tela do jogo
        self.screen = screen                    
        self.options = ["Iniciar Jogo", "Sair"]                              # Opções a serem escritas
        self.selected = 0                                                    # começa selecionando "Iniciar jogo"
        self.font = pygame.font.Font(None, 100)                              # Carrega a fonte a ser usada
        self.start_time = time.time()                                        # Começa o tempo da animação
        self.y_positions = [-100, -50]                                       # Início fora da tela
        self.animation_speed = 5                                             # Velocidade da animação
        self.background = background                                         # Carregar imagem de fundo
        self.background = pygame.transform.scale(self.background, (800, 600))  # Ajustar ao tamanho da tela
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))  # Desenhar imagem de fundo
        
        current_time = time.time()
        blink = int(current_time * 2) % 2  # Piscar o texto "Pressione Enter"
        
        # Animação de entrada
        for i in range(len(self.y_positions)):
            if self.y_positions[i] < 300 + i * 80:
                self.y_positions[i] += self.animation_speed
        
        screen_width = self.screen.get_width()
        
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_width = text.get_width()
            x_position = (screen_width - text_width) // 2  # Centraliza horizontalmente
            self.screen.blit(text, (x_position, self.y_positions[i]))
        
        if blink:
            hint_text = self.font.render("Echoes of the forest", True, (255, 0, 0))
            hint_width = hint_text.get_width() 
            x_hint = (screen_width - hint_width) // 2
            self.screen.blit(hint_text, (x_hint, 500))
        
        pygame.display.flip()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected  # Retorna a opção selecionada
        return None


