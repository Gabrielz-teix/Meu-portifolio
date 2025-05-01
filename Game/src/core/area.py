from src.core.map import Map
from src.data.objects import create_entity

area = None # Variavel que vai receber o mapa
map_folder_location = "content/maps" # Local onde encontramos os mapas

# Classe Area, responsável por carregar o mapa e os blocos
class Area: 
    def __init__(self, area_file, tile_types): # Chamamos o arquivo do mapa e os blocos
        global area
        area = self
        self.tile_types = tile_types
        self.load_file(area_file)
        
    def load_file(self, area_file):
        # Lê os arquivos inseridos em data.py
        
        file = open(map_folder_location + "/" + area_file, "r")
        data = file.read()
        file.close()

        # Separa as informações do mapa em blocos (acima do sinal de '-') e objetos (abaixo do sinal de '-')
        chunks = data.split('-')
        tile_map_data = chunks[0] # Blocos 
        entity_data = chunks[1]   # Objetos

        # Carrega o mapa na area, agora chamamos area.map
        self.map = Map(tile_map_data, self.tile_types)

        # Carrega os objetos 
        self.entities = []                                                          # Lista de entidades
        self.entity_lines = entity_data.split('\n')[1:]                             # Separa as linhas que implementam os objetos
        for line in self.entity_lines:                                              # Loop para as linhas dos objetos
            try:
                self.items = line.split(',')                                        # Separamos as infos de cada objeto por ','
                id = int(self.items[0])                                             # Id do objeto
                self.x = int(self.items[1])                                         # Posição x
                self.y = int(self.items[2])                                         # Posição y
                self.entities.append(create_entity(id, self.x, self.y, self.items)) # Adiciona a entidade na lista de entidades ativas 
            
            # Aqui detectamos os erros de ortografia no mapa, foi muito usado até chegarmos onde queriamos
            except ValueError as e:
                print(f"ValueError parsing line: {line} -> {e}")
            except IndexError as e:
                print(f"IndexError parsing line: {line} -> {e}")
            except Exception as e:
                print(f"Unexpected error parsing line: {line} -> {e}")



