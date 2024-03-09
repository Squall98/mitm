import xml.etree.ElementTree as ET
from urllib.parse import unquote
from map.contants import *
from map.cell import Cell

class Map():

    def __init__(self, interface):
        self.interface = interface
        self.cells = []
        self.binairemap = []
        self.carreau = []
        self.mapswidth = 0
        self.sun = []
        self.entity = []
        self.resource = []

    def extract_info_from_xml(self, xml_path):
        # Parse le fichier XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Crée un dictionnaire pour stocker les informations extraites
        info = {
            'ID': root.findtext('ID'),
            'Width': int(root.findtext('ANCHURA')),
            'Height': int(root.findtext('ALTURA')),
            'X': int(root.findtext('X')),
            'Y': int(root.findtext('Y')),
            'MapData': root.findtext('MAPA_DATA')
        }

        return info

    def extract_map_data_from_xml(self, xml_path):
        # Parse le fichier XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extrayez les données de la carte à partir de la balise MAPA_DATA
        map_data = root.findtext('MAPA_DATA')
        if map_data:
            print("mapData trouve:", map_data)
            return map_data
        else:
            print("mapData n'a pas ete trouve.")
            return None

    def data(self, mapID, map_date):
        self.mapID = mapID
        self.map_date = map_date
        # Mettez à jour le chemin pour pointer vers le fichier XML dans le répertoire 'maps'
        self.path = f'./resource/maps/{mapID}.xml'
        print("Ouverture du fichier XML :", self.path)

        # Utilisez la fonction pour extraire les informations et les données de la carte
        info = self.extract_info_from_xml(self.path)
        self.width = info.get('Width')
        self.height = info.get('Height')
        map_data = info.get('MapData')

        print("Width :", self.width)
        print("Height :", self.height)
        print("MapData :", map_data)

        # Traitez les données de la carte pour créer des objets Cell
        if map_data:
            self.create_cells_from_map_data(map_data)
        else:
            print("Aucune donne de carte trouve.")
            self.cells = []

        self.x = int(info.get('X'))
        self.y = int(info.get('Y'))

    def create_cells_from_map_data(self, map_data):
        # Découpez les données de la carte en blocs de 10 caractères, chaque bloc représentant une cellule
        cell_data_blocks = [map_data[i:i + 10] for i in range(0, len(map_data), 10)]

        # Créez des objets Cell pour chaque bloc de données
        self.cells = [Cell(block, CellID) for CellID, block in enumerate(cell_data_blocks)]


