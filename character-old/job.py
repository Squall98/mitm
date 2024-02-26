from character.path_finding import *


# Fonction pour récolter une ressource sur une cellule spécifique
def recole(character, cell):
    # Vérifie si la cellule est interactive
    if not character.map.carreau[cell]["cell"].isInteractive:
        return


    # Vérifie si la cellule ne contient pas d'entité ou contient un joueur
    if character.map.carreau[cell]["cell"].entity == [] or character.map.carreau[cell]["cell"].entity.type == "Player":
        bad_cell = []
        close_cell = get_close_cell(character.map,cell,bad_cell)
        bad_cell = []  # Liste pour garder en mémoire les cellules inaccessibles
        # Trouve la cellule la plus proche accessible
        close_cell = get_close_cell(character.map, cell, bad_cell)
        while True:
            if character.deplacement.deplacement(character.cell.CellID, from_pos_x_y_to_cell_id(close_cell[1][1], close_cell[1][0], character.map.mapswidth), character.map.mapswidth, character.map.carreau, character.map.binairemap, character.map.sun, character.map.resource)[0]:
                break
            else:
                if close_cell == (1000,None):
                    character.map.carreau[cell].isInteractive = False#A changer
                # Si le déplacement échoue, marque la cellule comme inaccessible et cherche une nouvelle cellule
                if close_cell == (1000, None):
                    character.map.carreau[cell].isInteractive = False  # Marque la cellule comme non interactive
                    return False
                bad_cell.append(close_cell)
                close_cell = get_close_cell(character.map, cell, bad_cell)
        # Obtient le type de la cellule pour envoyer le paquet de récolte
        celltype = get_id(character.map.carreau[cell]["cell"].layerObject2Num)
        packet = "GA500"+str(cell)+";"+celltype[-1]
        character.socket_to_server.send((packet+"\n\x00").encode())
        packet = "GA500" + str(cell) + ";" + celltype[-1]
        character.socket_to_server.send((packet + "\\n\\x00").encode())
        return True
    else:
        print("Monster one cell")
        print("Monster one cell")  # Un monstre occupe la cellule
        return False


# Fonction pour trouver la cellule accessible la plus proche
def get_close_cell(map, cell, bad_cell):
    endcell = from_cell_id_to_x_y_pos(cell, map.mapswidth)
    close_cell = (1000, None)
    for i in range(len(map.binairemap)):
        for j in range(len(map.binairemap[i])):
            distance = heuristic((j, i), endcell)
            if i % 2 == 0:
                distance -= 0.5  # Ajustement pour les lignes paires
            if endcell != (j, i) and distance < close_cell[0] and (distance, (i, j)) not in bad_cell:
                close_cell = (distance, (i, j))
    print(from_pos_x_y_to_cell_id(close_cell[1][1], close_cell[1][0], map.mapswidth))
    return close_cell


# Fonction pour obtenir l'identifiant de la ressource à partir d'un fichier
def get_id(id):
    with open("./resource/Recolte.txt", "r") as f:
        contenu = f.read()
    for ligne in contenu.split():
        ligne = ligne.split("|")
        if ligne[0] == str(id):
            return ligne


if __name__ == "__main__":
    print(get_id(7500))
