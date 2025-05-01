from pygame import Rect

bodies = [] # Lista de objetos com física presentes no mapa

# Classe para a física de cada Objeto
class Body: 
    def __init__(self, x=0, y=0, width=32, height= 32): # Recebe uma posição e dimensões do objeto
        self.hitbox = Rect(x,y, width, height)          # Cria um hitbox dentro das infos passadas
        bodies.append(self)                             # adiciona o corpo na lista
    
    # Função para checar se a posição é válida
    def is_position_valid(self):                                        
        from Jogo.src.core.map import map    
        x = self.entity.x + self.hitbox.x                                   # Guarda a posição do hitbox do objeto e de um corpo
        y = self.entity.y + self.hitbox.y
        if map.is_rect_solid(x,y,self.hitbox.width, self.hitbox.height):    # Caso o corpo seja solido a posição não será válida
            return False
        for body in bodies:
            if body != self and body.is_colliding_with(self):               # Caso haja uma colisão do jogador com um objeto não será válida
                return False
        if self.entity.x > 4752 or self.entity.x < -26 or self.entity.y > 1720 or self.entity.y < -46: # Prende o Jogador no mapa
            return False
        return True # Caso nada disso seja comprovado, a posição será válida
    
    def is_colliding_with(self, other):             # Função que checa se há colisão
        x = self.entity.x + self.hitbox.x           # Guarda a posição de um corpo com a hitbox 
        y= self.entity.y + self.hitbox.y
        other_x = other.entity.x + self.hitbox.x    # Guarda a nossa posição com a hitbox de um corpo
        other_y = other.entity.y + other.hitbox.y
        
        if x < other_x + other.hitbox.width and \
            x + self.hitbox.width > other_x and \
                y < other_y + other.hitbox.height and\
                    y + self.hitbox.height > other_y:   # Caso a posição seja menor que a soma da posição com o hitbox de um corpo e caso
                            return True                 # a posição seja menor que a hitbox com a posição de um corpo há colisão 
        else:
            return False                                # Caso contrário não há colisão
    
def reset_bodies():                                     # Função para resetar os corpos do mapa, usada em restart_game()
        global bodies
        bodies = []