import pygame

active_objs = []

# O arquivo define uma entidade genérica no jogo.
# Uma entidade é um objeto que pode conter diversos componentes para definir seu comportamento, aparência ou outras funcionalidades.

class Entity:
    def __init__(self, *components, x=0, y=0, width=32, height=32): # *components permite lançar quantos parâmetros quisermos
        self.components = []
        self.fps = 12
        self.clock = pygame.time.Clock()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        for c in components: 
            self.add(c)

    def add(self, component): # Adiciona um componente à entidade.
        component.entity = self
        self.components.append(component)

    def remove(self, kind):   # Remove um componente da entidade
        c = self.get(kind)
        if c is not None:
            c.entity = None
            self.components.remove(c)

    def get(self, kind):    # Pega um componente da entidade
        for c in self.components:
            if isinstance(c, kind):
                return c
        return None    

    def get_rect(self):     # Retorna um retângulo representando a entidade
        return pygame.Rect(self.x, self.y, self.width, self.height)
