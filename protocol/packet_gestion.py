from character.character import Character
from map.map_frame import MapFrame
from map.combat import Combat
import threading
from script import Script

# Classe de gestion des paquets réseau
class PacketGestion():

    # Constructeur
    def __init__(self, interface, socket_to_server):
        # Initialisation du personnage, de l'interface, et du socket serveur
        self.character = Character(interface, socket_to_server)
        self.interface = interface
        self.socket_to_server = socket_to_server
        # Association du personnage à l'interface utilisateur
        self.interface.set_character(self.character)
        # Initialisation des composants relatifs à la carte et au combat
        self.map_frame = MapFrame(interface, self.character)
        self.combat = Combat(self.map_frame)
        # Initialisation d'un script associé au personnage
        self.script = Script(self.character)

    # Méthode pour définir le socket serveur
    def set_socket(self, socket_to_server):
        self.socket_to_server = socket_to_server
        self.character.set_socket(self.socket_to_server)
        # La ligne commentée semble être une ancienne tentative de définir le socket pour la carte

    # Méthode de traitement des paquets serveur
    def server_packet(self, packet):
        # Traitement des informations du personnage
        if packet[:3] == "ASK":
            info_perso = packet[3:].split("|")
            self.character.base(id_=info_perso[1], pseudo=info_perso[2], lvl=info_perso[3], id_class=info_perso[4],
                                sexe=info_perso[5], gfx=info_perso[6])
            self.interface.ongletsPersonnage.create_charater(self.character.gfx, self.character.pseudo,
                                                             self.character.id_, self.character.lvl)
        # Mise à jour des sorts du personnage
        elif packet[:2] == "SL" and packet[2:4] != "o+":
            spells_data = packet[2:].split(";")
            self.character.spells.update_spells(spells_data)
        # Mise à jour des statistiques du personnage
        elif packet[:2] == "As":
            self.character.character_stats(packet[2:].split("|"))
            self.interface.base_start(self.character)
            self.interface.ongletsPersonnage.create_label_caracteristique(self.character)

        # Traitement des informations de la carte
        elif packet[:3] == "GDM":
            data = packet.split("|")
            mapID, map_date = data[1], data[2]  # Suppression de la référence à decryption_key
            self.character.map.data(mapID, map_date)  # Mise à jour de l'appel à la méthode .data
            self.interface.ongletsMap.print_map(self.character.map)

        # Gestion des entités sur la carte
        elif packet[:2] == "GM":
            self.map_frame.parse_data(packet)
        elif packet[:3] == "GDF" and len(packet) > 7:
            self.map_frame.update_interactive(packet)

        # Gestion du combat et des mouvements des entités
        elif self.character.entity:
            if packet[:2] == "GA":
                self.map_frame.update_entity(packet)
            elif packet[:3] == "GIC":
                self.combat.mouv_start_cell(packet)
            elif packet[:2] == "GE":
                self.character.isfighting = False
            elif packet[:3] == "GTM":
                self.combat.update_carac_entity(packet)
            elif packet[:3] == "GTS":
                data = packet[3:].split("|")
                if data[0] == self.character.id_:
                    print("ID030""debut du tour...")
                    threading.Thread(None, self.combat.fight).start()
