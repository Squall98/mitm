from character.path_finding import *
import time, random

# Classe Combat définissant la logique et les interactions de combat dans le jeu
class Combat:

    # Initialisation de la classe avec la carte du jeu
    def __init__(self, map_frame):
        self.map_frame = map_frame

    # Début du mouvement d'une entité sur la carte
    def mouv_start_cell(self, packet):
        packet = packet[4:].split(";")
        entity_id = int(packet[0])  # ID de l'entité
        cell = packet[1]  # Cellule de départ
        # Mise à jour de la position de l'entité sur la carte
        self.map_frame.entity_gestion.update_entity(entity_id, int(cell))

    # Mise à jour des caractéristiques d'une entité
    def update_carac_entity(self, packet):
        for data in packet[4:].split("|"):
            data = data.split(";")
            entity_id = data[0]  # ID de l'entité
            if data[1] == "0":  # Vérification si l'entité est en vie
                vie = data[2]  # Points de vie
                pa = data[3]  # Points d'action
                pm = data[4]  # Points de mouvement
                cell_id = data[5]  # ID de la cellule
                vie_max = data[7]  # Points de vie maximum
                # Mise à jour des caractéristiques de l'entité
                self.map_frame.entity_gestion.update_carac_entity(entity_id, vie, pa, pm, cell_id, vie_max)

    # Logique de combat
    def fight(self):
        time.sleep(random.uniform(0, 1.5))  # Pause aléatoire pour simuler un délai de combat
        # Position du joueur
        pos_player = from_cell_id_to_x_y_pos(self.map_frame.character.cell.CellID,
                                             self.map_frame.character.map.mapswidth)
        dist = 999999  # Distance initiale très élevée

        # Boucle à travers les entités pour trouver la cible la plus proche
        for noob in self.map_frame.entity_gestion.entity:
            if noob.id == int(self.map_frame.character.id_):
                continue  # Ignorer l'entité si c'est le joueur lui-même
            pos_entity = from_cell_id_to_x_y_pos(int(noob.cell), self.map_frame.character.map.mapswidth)
            x = heuristic(pos_entity, pos_player)  # Calcul de la distance
            if x < dist:  # Mise à jour de la distance si une cible plus proche est trouvée
                dist = x
                # Ajustement de la distance basé sur les positions
                if pos_entity[1] % 2 == 0 and pos_player[1] % 2 != 0:
                    dist += 0.5
                elif pos_entity[1] % 2 != 0 and pos_player[1] % 2 == 0:
                    dist += 0.5
                good_pos = pos_entity  # Mise à jour de la position de la cible

        # Décision de lancer un sort avant de bouger
        lauch_spell_before = True
        if dist <= 8:
            lauch_spell_before = False
            pos_entity = good_pos
            dist = 0
            for cell in self.map_frame.character.map.cells:
                if cell.isActive:
                    # La logique pour déterminer si le joueur peut lancer un sort ou doit se déplacer
                    cell_test = from_cell_id_to_x_y_pos(cell.CellID, self.map_frame.character.map.mapswidth)
                    x = heuristic(cell_test, pos_entity)
                    if dist < x:
                        good_pos = cell_test
                        dist = x
                    # est tronquée pour cet exemple.

    # Lancement d'un sort
    def launch_spell(self, spells_id=(161, 163)):
        dist = 99999  # Distance initiale très élevée
        # Boucle à travers les sorts disponibles
        for spell_id in spells_id:
            for noob in self.map_frame.entity_gestion.entity:
                if noob.id == int(self.map_frame.character.id_):
                    continue  # Ignorer l'entité si c'est le joueur lui-même
                pos_entity = from_cell_id_to_x_y_pos(int(noob.cell), self.map_frame.character.map.mapswidth)
                x = heuristic(pos_entity, from_cell_id_to_x_y_pos(self.map_frame.character.cell.CellID,
                                                                  self.map_frame.character.map.mapswidth))
                if x < dist:  # Mise à jour de la distance si une cible plus proche est trouvée
                    dist = x
                    good_pos = noob.cell  # Mise à jour de la position de la cible

            # Envoi du sort au serveur pour l'exécuter sur la cible
            print(f"Lancement du sort {spell_id}, sur la cell {good_pos}")
            self.map_frame.character.socket_to_server.send((f"GA300{spell_id};{good_pos}" + "\n\x00").encode())
            time.sleep(random.uniform(1.2, 2.3))  # Pause pour simuler le temps de lancement du sort

# Bloc principal pour tester les fonctionnalités si le script est exécuté directement
if __name__ == "__main__":
    import os
    from lxml import etree

    spells_id = (161, 163)  # Identifiants des sorts
    path = os.getcwd() + "\\resource\\spells.xml"  # Chemin vers le fichier des sorts
    tree = etree.parse(path)  # Parsing du fichier XML des sorts
    for spell in spells_id:
        for spell in tree.xpath("/SPELLS/SPELL"):
            if "151" == spell.get("ID"):
                spell_name = spell.get("ID").get("LEVEL").text
                print(spell_name)  # Affichage du nom du sort
