from character.path_finding import *
from threading import Thread
import time


# Définition de la classe Deplacement
class Deplacement():

    # Constructeur de la classe
    def __init__(self, socket_to_server):
        self.ismouving = False  # Indicateur de mouvement
        self.socket_to_server = socket_to_server  # Socket pour communiquer avec le serveur

    # Méthode pour déplacer le personnage
    def deplacement(self, cell_base, cell_clic, width, carreau, binairemap, sun, resource, pm=None, combat=False):
        # Conversion des cellules de départ et d'arrivée en coordonnées x, y
        cell_start = from_cell_id_to_x_y_pos(cell_base, width)
        cell_end = from_cell_id_to_x_y_pos(carreau[cell_clic]["cell"].CellID, width)

        # Vérifie si la cellule de départ est la même que la cellule d'arrivée
        if cell_start == cell_end:
            return True

        # Ajuste la binairemap en fonction des cellules ensoleillées ou contenant des ressources
        if carreau[cell_clic]["cell"].CellID in sun:
            binairemap[cell_end[1]][cell_end[0]] = 0
        elif carreau[cell_clic]["cell"].CellID in resource:
            binairemap[cell_end[1]][cell_end[0]] = 1

        # Conversion de la carte en array numpy pour l'utilisation avec A*
        numpy_ = from_array_map_to_numpy(binairemap, width)
        # Calcul du chemin avec A*
        astar_path = astar(numpy_, cell_start, cell_end, combat)

        if astar_path != False:
            # Limite le chemin à la portée de mouvement si spécifié
            if pm:
                astar_path = astar_path[:pm + 1]

            # Calcul du temps nécessaire pour le déplacement
            run_timing = timing(astar_path)
            # Conversion du chemin A* en chemin utilisable dans Dofus
            dofus_path = convert_astar_path_to_dofus_path(astar_path, width)

            self.ismouving = True  # Indique que le personnage se déplace
            # Gestion du déplacement en fonction du mode combat ou non
            if combat:
                self.wait(dofus_path, run_timing, from_pos_x_y_to_cell_id(astar_path[-1][0], astar_path[-1][1], width))
            else:
                Thread(None, self.wait, args=[dofus_path, run_timing,
                                              from_pos_x_y_to_cell_id(astar_path[-1][0], astar_path[-1][1],
                                                                      width)]).start()
            return (True, run_timing)

        return (False, 0)  # Le déplacement n'a pas pu être effectué

    # Méthode pour gérer l'attente pendant le déplacement
    def wait(self, dofus_path, run_timing, last_cell):
        print(f"Déplacement du personnage vers {last_cell} (temps {run_timing})")
        # Envoi du paquet de déplacement au serveur
        packet = "GA001" + dofus_path[0] + "\\n\\x00"
        self.socket_to_server.send(packet.encode())
        time.sleep(run_timing)  # Attente pour simuler le déplacement
        # Envoi d'un paquet pour indiquer la fin du déplacement
        self.socket_to_server.send(("GKK0" + "\\n\\x00").encode())
        self.ismouving = False  # Indique que le déplacement est terminé
        print("Fin du déplacement")
