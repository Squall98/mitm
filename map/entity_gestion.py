import copy


class EntityGestion:
    def __init__(self, interface):
        self.map = interface.ongletsMap
        self.character = self.map.character
        self.entities = []

    def clear_entities(self):
        for cell in self.map.cells:
            cell.clear_entities()
        self.entities.clear()

    def add_entity(self, entity):
        cell = self.character.map.find_cell_by_id(entity.cell)
        if entity not in cell.entities:
            cell.add_entity(entity)
            self.entities.append(entity)
            if self.character.id_ == entity.id:
                self.character.cell = cell
                self.character.entity = entity

    def remove_entity(self, entity):
        cell = self.character.map.find_cell_by_id(entity.cell)
        cell.remove_entity(entity)
        self.entities.remove(entity)

    def update_entity_position(self, entity_id, new_cell_id):
        entity = self.find_entity_by_id(entity_id)
        if entity:
            old_cell = self.character.map.find_cell_by_id(entity.cell)
            new_cell = self.character.map.find_cell_by_id(new_cell_id)
            if old_cell:
                old_cell.remove_entity(entity)
            if new_cell:
                new_cell.add_entity(entity)
                entity.cell = new_cell_id

    def update_entity_stats(self, entity_id, vie, pa, pm, vie_max):
        entity = self.find_entity_by_id(entity_id)
        if entity:
            entity.update_stats(vie, pa, pm, vie_max)

    def find_entity_by_id(self, entity_id):
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None

    def update_interactive_status(self, cell_id, is_interactive):
        cell = self.character.map.find_cell_by_id(cell_id)
        if cell:
            cell.is_interactive = is_interactive