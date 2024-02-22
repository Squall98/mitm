from character.spell import Spells
from character.deplacement import Deplacement
from map.map import Map

# Définition de la classe Character
class Character():

    # Constructeur de la classe
    def __init__(self, interface, socket_to_server):
        self.isharvest = False  # Indique si le personnage est en train de récolter
        self.isfighting = False  # Indique si le personnage est en combat
        self.spells = Spells(interface)  # Gestion des sorts du personnage
        self.map = Map(interface)  # Gestion de la carte sur laquelle le personnage évolue
        self.interface = interface  # Interface utilisateur
        self.socket_to_server = socket_to_server  # Socket pour la communication avec le serveur
        self.deplacement = Deplacement(self.socket_to_server)  # Gestion des déplacements
        self.entity = None  # Entité représentant le personnage

    # Méthode pour définir la cellule sur laquelle le personnage se trouve
    def set_cell(self, cell):
        self.cell = cell

    # Méthode pour initialiser les informations de base du personnage
    def base(self, id_, pseudo, lvl, id_class, sexe, gfx):
        self.id_, self.pseudo, self.lvl, self.id_class, self.sexe, self.gfx = id_, pseudo, lvl, id_class, sexe, gfx

    # Méthode pour mettre à jour les statistiques du personnage à partir des données reçues
    def character_stats(self, data):
        # XP actuelle, XP au début du niveau actuel, et XP pour le prochain niveau
        self.xp_actuelle = data[0].split(",")[0]
        self.xp_depart = data[0].split(",")[1]
        self.xp_fin = data[0].split(",")[2]

        # Kamas possédés par le personnage
        self.kamas = data[1]

        # Points de sorts disponibles
        self.points_sorts = data[2]

        # Vie actuelle et vie maximale du personnage
        self.vie_actuelle = data[5].split(",")[0]
        self.vie_max = data[5].split(",")[1]

        # Énergie actuelle et énergie maximale
        self.ennergie_actuelle = data[6].split(",")[0]
        self.ennergie_max = data[6].split(",")[1]

        # Points d'Action (PA) disponibles pour le personnage
        self.PA = data[9].split(",")[4]

        # Points de Mouvement (PM) disponibles pour le personnage
        self.PM = data[10].split(",")[4]

        # Calcul des caractéristiques de force
        carac = data[11].split(",")
        self.force = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])

        # Calcul des caractéristiques de vitalité
        carac = data[12].split(",")
        self.vita = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])

        # Calcul des caractéristiques de sagesse
        carac = data[13].split(",")
        self.sagesse = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])

        # Calcul des caractéristiques de chance
        carac = data[14].split(",")
        self.chance = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])

        # Calcul des caractéristiques d'agilité
        carac = data[15].split(",")
        self.agi = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])

        # Calcul des caractéristiques d'intelligence
        carac = data[16].split(",")
        self.intel = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])

        # Calcul de la portée (PO)
        carac = data[17].split(",")
        self.PO = int(carac[0]) + int(carac[1]) + int(carac[2]) + int(carac[3])
