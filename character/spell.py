# Importation de la bibliothèque lxml pour le parsing de fichiers XML
from lxml import etree
import os


# Définition de la classe Spells
class Spells():

    # Constructeur de la classe avec une interface en paramètre
    def __init__(self, interface):
        self.interface = interface
        self.list_spell = {}  # Dictionnaire pour stocker les sorts

    # Méthode pour mettre à jour les sorts à partir des données fournies
    def update_spells(self, spells_data):
        # Supprime les sorts existants dans l'interface
        self.interface.ongletsSorts.removes_spells()
        # Itère sur les données des sorts reçues, en excluant le dernier élément
        for spell in spells_data[:len(spells_data) - 1]:
            spell = spell.split("~")  # Sépare les informations du sort
            # Met à jour l'interface avec les informations du sort
            self.interface.ongletsSorts.add_spell(spell[0], self.get_name(spell[0]), spell[1])

    # Méthode pour obtenir le nom d'un sort à partir de son identifiant
    def get_name(self, id_):
        # Construction du chemin vers le fichier XML contenant les informations des sorts
        dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource/spells.xml")
        spell_name = "None"  # Nom du sort par défaut
        tree = etree.parse(dir_path)  # Parse le fichier XML

        # Recherche le sort correspondant à l'identifiant donné dans le fichier XML
        for spell in tree.xpath("/SPELLS/SPELL"):
            if id_ == spell.get("ID"):
                spell_name = spell.find("NAME").text  # Obtient le nom du sort

        return spell_name  # Retourne le nom du sort
