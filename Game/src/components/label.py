import pygame

fonts = {}        # Carrega as fontes
anti_alias = True # Diminui o serrilhado delas

labels = []       # Lista de escritos no jogo

font_folder_path = "content/fonts" # Caminho de onde as fontes estão

# Classe de escritos do jogo
class Label:
    def __init__(self, font, text, size=32, color=(255, 255, 255)):           # Parametros de fonte usada, texto escrito, tamanho e cor
        global labels                                                         # Torna global para ser usada depois 
        self.color = color
        if font in fonts:                                                     # Se a fonte já esta carrega não carregamos ela mais
            self.font = fonts[font]
        else:
            self.font = pygame.font.Font(font_folder_path + "/" + font, size) # Se não nós carregamos
            # self.font = pygame.font.SysFont(font, size)

        self.set_text(text) # Aqui colocamos o texto e adicionamos ele na lista de escritos
        labels.append(self)

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.color)

    def draw(self, screen): # Aqui desenhamos o texto
        screen.blit(self.surface, (self.entity.x, self.entity.y))