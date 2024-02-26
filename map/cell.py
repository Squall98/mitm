from map.contants import *


def unhash_cell(raw_cell):
    try:
        return [ZKARRAY.index(i) for i in raw_cell]
    except ValueError as e:
        raise ValueError(f"Caractere inconnu dans les donnees de la cellule: {e}")



class Cell:
    def __init__(self, raw_data, CellID):
        self.raw_data = raw_data
        self.entity = []
        self.color = 'black'
        self.CellID = CellID
        cell_data = unhash_cell(raw_data)
        self.isActive = self.calculate_active(cell_data)
        self.isInteractive = ((cell_data[7] & 2) >> 1) != 0
        self.lineOfSight = (cell_data[0] & 1) == 1
        self.layerGroundRot = cell_data[1] & 48 >> 4
        self.groundLevel = cell_data[1] & 15
        self.movement = ((cell_data[2] & 56) >> 3)
        self.layerGroundNum, self.layerObject1Num, self.layerObject2Num = self.calculate_layers(cell_data)
        self.isSun = self.layerObject1Num in SUN_MAGICS or self.layerObject2Num in SUN_MAGICS
        self.text = str(self.movement)
        self.set_default_color()

    def calculate_active(self, cell_data):
        inactive_conditions = cell_data[2] == 0 or cell_data[0] in [1, 33] and cell_data[2] == 1
        return not inactive_conditions and (cell_data[0] & 32 >> 5) != 0

    def calculate_layers(self, cell_data):
        layer_ground_num = (cell_data[0] & 24 << 6) + (cell_data[2] & 7 << 6) + cell_data[3]
        layer_object_1_num = ((cell_data[0] & 4) << 11) + ((cell_data[4] & 1) << 12) + (cell_data[5] << 6) + cell_data[6]
        layer_object_2_num = ((cell_data[0] & 2) << 12) + ((cell_data[7] & 1) << 12) + (cell_data[8] << 6) + cell_data[9]
        return layer_ground_num, layer_object_1_num, layer_object_2_num

    def set_default_color(self):
        if self.entity != []:
            self.color = 'red'
        elif self.isSun:
            self.color = 'yellow'
            self.text = 'S'
        elif self.isInteractive:
            self.text = ' '
            self.color = 'green'
        elif self.isActive:
            self.text = ' '
            self.color = 'white'

    def get_entity(self, entity_id):
        return next((entity for entity in self.entity if entity.id == entity_id), None)

    def set_entity(self, entity, action):
        if action:
            if entity.isMainCharacter == True:
                self.color = 'blue'
                self.text = entity.type[0]
                self.entity.append(entity)
            else:
                self.color = 'red'
                self.text = entity.type[0]
                self.entity.append(entity)
        else:
            for i in range(len(self.entity)):
                if self.entity[i].id == entity.id:
                    self.entity.remove(self.entity[i])
                    self.set_default_color()
                    break

    def set_not_interactive(self, good):
        if good:
            self.color = 'green'
            self.isInteractive = True
        else:
            self.color = 'brown'
            self.isInteractive = False

    def __str__(self):
        return self.text