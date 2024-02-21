from map.contants import *
import yaswfp.swfparser as swfparser
from map.cell import Cell
from urllib.parse import unquote

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

    def extract_info(self, tags):
        info = {
            'ID': None, 'Width': None, 'Height': None, 'BackgroundNum': None,
            'AmbianceId': None, 'MusicId': None, 'Capabilities': None
        }
        constant_pool = None
        for tag in tags:
            if hasattr(tag, 'Actions'):
                for action in tag.Actions:
                    if action.name == "ActionConstantPool":
                        constant_pool = action.ConstantPool
                    elif action.name == "ActionPush" and hasattr(action, 'Integer'):
                        value = action.Integer
                        next_action_index = tag.Actions.index(action) + 1
                        if next_action_index < len(tag.Actions):
                            next_action = tag.Actions[next_action_index]
                            if next_action.name == "ActionSetVariable":
                                if info['ID'] is None:
                                    info['ID'] = value
                                elif info['Width'] is None:
                                    info['Width'] = value
                                elif info['Height'] is None:
                                    info['Height'] = value
                                elif info['BackgroundNum'] is None:
                                    info['BackgroundNum'] = value
                                elif info['AmbianceId'] is None:
                                    info['AmbianceId'] = value
                                elif info['MusicId'] is None:
                                    info['MusicId'] = value
                                elif info['Capabilities'] is None:
                                    info['Capabilities'] = value
        return info

    def extract_map_data(self, tags):
        for tag in tags:
            if hasattr(tag, 'Actions'):
                for action in tag.Actions:
                    if action.name == "ActionConstantPool":
                        constant_pool = action.ConstantPool
                        if 'mapData' in constant_pool:
                            map_data_index = constant_pool.index('mapData') + 1
                            if map_data_index < len(constant_pool):
                                map_data = constant_pool[map_data_index]
                                print("mapData trouvé:", map_data)
                                return map_data
        print("mapData n'a pas été trouvé.")
        return None

    def data(self, mapID, map_date, decryption_key):
        self.mapID = mapID
        self.map_date = map_date
        self.decryption_key = decryption_key
        MAP_DIR = (PATH + "/data/maps")
        self.path = f'{MAP_DIR}/{mapID}_{map_date}{"X" if decryption_key else ""}.swf'
        print("Ouverture du fichier SWF :", self.path)

        swf = swfparser.parsefile(self.path)
        info = self.extract_info(swf.tags)
        map_data_encrypted = self.extract_map_data(swf.tags)

        self.width = info.get('Width')
        self.height = info.get('Height')

        print("Width :", self.width)
        print("Height :", self.height)
        print("Encrypted MapData :", map_data_encrypted)

        # Après le décryptage des données de la carte
        if map_data_encrypted:
            map_data_decrypted = self.decrypt_mapdata(map_data_encrypted, decryption_key)
            print("Decrypted MapData :", map_data_decrypted)
        else:
            print("No MapData found or decryption key is missing.")
            self.cells = []

        pos = MAPID_TO_POS.get(mapID, (None, None))
        self.x = pos[0]
        self.y = pos[1]

    def decrypt_mapdata(self, raw_data, raw_key):
        key = unquote(''.join([chr(int(raw_key[i:i + 2], 16)) for i in range(0, len(raw_key), 2)]))
        print(f"Clé de décryptage: {key}")  # Affiche la clé de décryptage après conversion
        checksum = int(HEX_CHARS[sum(map(lambda x: ord(x) & 0xf, key)) & 0xf], 16) * 2
        print(f"Checksum calculé: {checksum}")  # Affiche le checksum calculé
        key_length = len(key)
        print(f"Longueur de la clé: {key_length}")  # Affiche la longueur de la clé
        data = ''
        for i in range(0, len(raw_data), 2):
            decoded_char = chr(int(raw_data[i:i + 2], 16) ^ ord(key[(int(i / 2) + checksum) % key_length]))
            data += decoded_char
            if i < 100:  # Limite l'affichage aux premiers caractères pour éviter une sortie trop longue
                print(f"Caractère décodé: {decoded_char}")  # Affiche les caractères décodés
        return data