import pygame
from Jogo.src.components.sprite import sprites, Sprite       # Importamos a nossa Classe Sprite e uma lista com as sprites ativas no jogo
from Jogo.src.components.player import Player                # ´´ a nossa Classe Jogador
from Jogo.src.components.entity import Entity, active_objs   # ´´ a Classe Entity e uma lista de objetos ativos no jogo
from Jogo.src.components.physics import Body, reset_bodies   # ´´ a Classe do corpo e uma função para resetá-los
from Jogo.src.core.input import keys_down                    # ´´ a função de identificar teclas apertadas
from Jogo.src.core.map import Map, TileKind, Key             # ´´ a Classe do mapa, a classe dos blocos do jogo e a classe da chave
from Jogo.src.core.camera import create_screen, camera       # ´´ a função de criar tela e a Classe camera
from Jogo.src.core.lanterna import Lanterna                  # ´´ a Classe Lanterna 
from Jogo.src.components.label import labels                 # ´´ uma lista com os escritos do jogo
from Jogo.src.core.area import area, Area                    # ´´ a Classe Area e a variavel que vai receber o arquivo do mapa
from Jogo.src.components.enemy import Enemy                  # ´´ a Classe do Fantasma
from Jogo.src.data.objects import entity_factories           # ´´ a lista com os objetos do jogo
from Jogo.src.components.menu import *                       # ´´ o Menu do jogo e as imagens das telas
from Jogo.src.core.sons import *                             # ´´ todos os sons do jogo
import math                                         # ´´ a biblioteca para fazer cálculos

# Função de restart
def restart_game(): 
    """Reinicia o estado do jogo."""
    global player, enemy, active_objs, sprites, labels # Declara as variaveis como globais para recebê-las

    # Limpar objetos antigos
    active_objs.clear()
    sprites.clear()
    labels.clear()
    area.entities.clear()
    area.entity_lines.clear()
    area.tile_types.clear()
    area.__dict__.clear()
    player.components.clear()
    enemy.components.clear()
    keys_down.clear()
    reset_bodies()
    som_vitoria.stop()
    som_game_over.stop()
    
    for sprite in sprites:
        sprite.kill()  # Remove o sprite de grupos

    menu.draw()
    
    # Reiniciar o jogo chamando a função principal
    main()
# Função da tela de Game Over
def game_over():
    """Tela de derrota"""
    # Para o som ao perder o jogo
    som_floresta.stop()  
    som_passo.stop()
    som_fantasma_perto.stop()
    
    som_game_over.set_volume(1.0)  
    som_game_over.play(loops=-1)  

    font = pygame.font.Font(None, 125)
    font2 = pygame.font.Font(None, 50)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text2 = font2.render("Pressione R para reiniciar", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (125, 250))
        screen.blit(text2, (185, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Pressionar R para reiniciar
                    restart_game()

        pygame.display.flip()
# Função da tela de Vitória
def you_win():
    """Exibe a tela de vitoria e espera o jogador decidir."""
    som_floresta.stop()  # Para o som ao ganhar o jogo
    som_passo.stop()
    som_fantasma_perto.stop()
    som_vitoria.set_volume(0.5)  # Ajuste o volume conforme necessário
    som_vitoria.play(loops=-1)  # -1 faz o som repetir indefinidamente
    font = pygame.font.Font(None, 125)
    font2 = pygame.font.Font(None, 50)
    text = font.render("YOU WIN", True, (0, 128, 0))
    text2 = font2.render("Pressione R para reiniciar", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (185, 250))
        screen.blit(text2, (185, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Pressionar R para reiniciar
                    restart_game()

        pygame.display.flip()
# Função principal do jogo
def main():
    """Função principal do jogo."""
    global player, enemy, running, screen, clear_color, lanterna, area, menu
    pygame.init()
    screen = create_screen(800, 600, "Echoes of the forest") # Usamos a função create_screen do camera.py para fazer a tela do jogo
    menu = Menu(screen)

    # Loop do Menu
    running_menu = True
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            selection = menu.handle_event(event)
            if selection == 0:  # Iniciar jogo
                running_menu = False
            elif selection == 1:  # Sair
                pygame.quit()
                exit()
    
        menu.draw()


# Define volume e toca em loop
    som_floresta.set_volume(0.05)  
    som_floresta.play(loops=-1)   

# Configurações gerais
    clear_color = (0, 0, 0, 255)             # Cor de fundo do jogo
    running = True                           # Enquanto running for True o jogo fica aberto
    clock = pygame.time.Clock()              # Clock para a animação do jogo
    trancado = True                          # Condição de vitória do jogador
    lanterna = Lanterna(raio=200, angulo=60, # Criação da lanterna e a tela usada para deixar o mapa escuro
                escurecimento=(0, 0, 0, 150)) 

    # Criação dos blocos do mapa
    tile_kinds = [ 
        TileKind("dirt", "../public/Jogo/content/images/dirt.png", False),      # 0 no mapa
        TileKind("grass", "../public/Jogo/content/images/grass.png", False),    # 1 no mapa
        TileKind("water", "../public/Jogo/content/images/water.png", True),     # 2 no mapa
        TileKind("wood", "../public/Jogo/content/images/madeira.png", False),   # 3 no mapa
        TileKind("gravel", "../public/Jogo/content/images/gravel.png", False)   # 4 no mapa
    ]

    # inicialização do mapa
    area = Area("start.map", tile_kinds)

    # Inicialização do jogador
    player = Entity(Player(), Body(20,45,20,10), x=32*11, y=32*7)
    enemy = Entity(Enemy(player), Body(0,0,0,0), x=32*15, y=32*5)


    key_image = pygame.image.load("../public/Jogo/content/images/chave.png")  
    chave = Key(4042, 1499, image=key_image)
    casa = Entity(Sprite("../public/Jogo/content/images/casa.png"), Body(-32,32,200,200), x=10, y=-80)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys_down.add(event.key)
                if event.key == pygame.K_f:
                    lanterna.ligada = not lanterna.ligada
                    som_lanterna.set_volume(0.5)  
                    som_lanterna.play(loops=0)  
            elif event.type == pygame.KEYUP:
                keys_down.discard(event.key)
            

        # Checa a colisão do fantasma com o jogador
        if math.sqrt((enemy.get(Enemy).x - player.x) ** 2 + (enemy.get(Enemy).y - player.y) ** 2) < 32:
            game_over()

        # Checa a colisão do jogado com a chave
        if chave.get_rect().colliderect(player.get_rect()) and not chave.collected:
            chave.collected = True
            som_chave.set_volume(0.5)  # Ajuste o volume conforme necessário
            som_chave.play(loops=0)  # -1 faz o som repetir indefinidamente
            
        # Condição de vitória do jogador
        if chave.collected and player.x == 97 and player.y == 119:
            you_win()
        # Loop de atualização dos objetos
        for a in active_objs:
            a.update()
        # Desenho do fundo do mapa com uma cor sólida e carregamento do mapa
        screen.fill(clear_color)
        area.map.draw(screen)
        # Desenho da chave no mapa
        if not chave.collected:
                chave.draw(screen, camera)

        # Loop para carregar as spites do jogo
        for s in sprites:
            s.draw(screen)
        # Desenha a lanterna e o jogador
        lanterna.desenhar(screen, player.x, player.y, player.width, player.height, camera.x, camera.y)
        player.get(Player).draw(screen)
        
        # Configuração para o fantasma só aparecer quando a lanterna apontar para ele
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Direção da lanterna (vetor normalizado)
        dir_x, dir_y = mouse_x - lanterna.lanterna_pos_x, mouse_y - lanterna.lanterna_pos_y
        angle_lanterna = math.atan2(dir_y, dir_x)  # Ângulo da lanterna

        if lanterna.ligada:
            enemy_obj = enemy.get(Enemy)
            dx = enemy_obj.x - player.x
            dy = enemy_obj.y - player.y
            dist_sq = dx**2 + dy**2  # Distância ao quadrado (evita usar sqrt)

            if dist_sq < lanterna.raio ** 2:  # Verifica se o inimigo está dentro do raio da lanterna
                angle_enemy = math.atan2(dy, dx)  # Ângulo entre jogador → inimigo
                diferenca_angulo = abs(angle_enemy - angle_lanterna)  # Diferença angular

                abertura = math.radians(30)  # Exemplo: 60° total, então 30° para cada lado

                if diferenca_angulo < abertura:
                    enemy_obj.draw(screen)  # Desenha o inimigo apenas se estiver no cone da lanterna
        
        # Loop para os escritos do jogo
        for l in labels:
            l.draw(screen)
        
        pygame.display.flip()
        clock.tick(16)

    pygame.quit()

if __name__ == "__main__":
    main()