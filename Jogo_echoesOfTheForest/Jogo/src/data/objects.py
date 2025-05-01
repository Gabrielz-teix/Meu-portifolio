from Jogo.src.components.entity import Entity 
from Jogo.src.components.sprite import Sprite
from Jogo.src.components.player import Player
from Jogo.src.components.physics import Body

# Lista de entidades, aqui fabricamos os objetos que vamos desenhar no nosso mapa
entity_factories = [
    # 0 = pedra
    lambda args: Entity(Sprite("Jogo/content/images/rock.png"), Body(-5,12,10,5)),
    
    # 1 = árvore
    lambda args: Entity(Sprite("Jogo/content/images/tree.png"), Body(16, 96, 32, 32)),      
    
    # 2 - árvore velha
    lambda args: Entity(Sprite("Jogo/content/images/tree2.png"), Body(16, 96, 32, 32)), 

    # 3 - árvore velha2
    lambda args: Entity(Sprite("Jogo/content/images/tree3.png"), Body(16, 96, 32, 32)),

    # 4 - poço
    lambda args: Entity(Sprite("Jogo/content/images/poço.png"), Body(500,50,60,50)),

    # 5 - casa
    lambda args: Entity(Sprite("Jogo/content/images/house.png"), Body(25, 65, 150, 170)),
]

# Função que usamos para criar o objeto com as características acima
def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e =  factory(data)
    e.x = x*32
    e.y = y*32
    return e