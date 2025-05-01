import pygame

# Modulo que guarda todos os sons usados no jogo

pygame.mixer.init()

som_floresta = pygame.mixer.Sound("content/sounds/floresta.mp3")
som_vitoria = pygame.mixer.Sound("content/sounds/victory.mp3")
som_chave = pygame.mixer.Sound("content/sounds/chave.mp3")
som_game_over = pygame.mixer.Sound("content/sounds/game_over.mp3")
som_lanterna = pygame.mixer.Sound("content/sounds/lanterna.mp3")
som_fantasma_perto = pygame.mixer.Sound("content/sounds/fantasma_perto.mp3")
som_fantasma = pygame.mixer.Sound("content/sounds/fantasma.mp3")
som_passo = pygame.mixer.Sound("content/sounds/passos.mp3")