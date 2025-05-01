import pygame

# O Módulo camera é responsável por seguir o jogador durante a gameplay

camera = pygame.Rect(0, 0, 0, 0) # Cria a camera que será um retangulo que irá cobrir toda a tela e será invisível

def create_screen(width, height, title):               # Função para criar a tela, já vamos chamar ela na main com essas infos e evitar muito codigo
    pygame.display.set_caption(title)                 # Colocamos o titulo
    screen = pygame.display.set_mode((width, height)) # Cria a tela usando os parâmetros de altura e largura
    camera.width = width                              # A variável camera passa ter a largura da tela
    camera.height = height                            # A variável camera passa ter a altura da tela
    return screen                                     # Retorna a camera

def update_camera(player_rect):                                               # Função para atualizar a camera com base na posição do jogador
    """
    Atualiza a posição da câmera para centralizar no jogador.
    :param player_rect: Um objeto pygame.Rect representando o jogador.
    """
    camera.x = player_rect.x + player_rect.width // 2 - camera.width // 2    # O x da camera será atualizado conforme o x do jogador
    camera.y = player_rect.y + player_rect.height // 2 - camera.height // 2  # O y da camera será atualizado conforme o y do jogador
    
    # Como queremos que o jogador fique centralizado na camera sempre, fazemos o seguinte calculo

