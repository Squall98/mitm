# Importation des bibliothèques nécessaires
from threading import Thread
import socket, time, fritm
from interface.main_interface import MainInterface
from protocol.packet_gestion import PacketGestion
from map.contants import PATH

# Définition de la classe MITM (Man In The Middle)
class MITM():
    # Constructeur de la classe
    def __init__(self, server_ip="127.0.0.1", server_port=6555, interface=None, packet_gestion=None):
        # Initialisation des variables d'instance
        self.server_port = server_port
        self.server_ip = server_ip
        self.interface = interface
        # Création des sockets pour la communication client et serveur
        self.socket_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Si aucune interface n'est fournie, une nouvelle est créée
        if self.interface == None:
            self._hook()
            self.interface = MainInterface()
        self.packet_gestion = PacketGestion(self.interface, self.socket_to_server)
        self.start_client()

    # Méthode pour démarrer la communication avec le client
    def start_client(self):
        try:
            self.socket_to_client.bind((self.server_ip, self.server_port))
        except:
            print(f"Can't bind for the client")

        self.socket_to_client.listen(1)
        self.connexion, adresse = self.socket_to_client.accept()
        print("Connection established...\nConnecting to server")

        self.listening_client()

    # Méthode pour démarrer la communication avec le serveur
    def start_server(self, adresse):
        try:
            self.socket_to_server.connect((adresse[0], int(adresse[1])))
            self.connexion.send(("HTTP/1.0 200 OK").encode())
            time.sleep(0.5)
        except:
            print(f"Can't bind the server")

        # Démarrage de l'écoute du serveur dans un nouveau thread
        Thread(None, self._boucle_recv_send, args=[self.socket_to_server, self.connexion, "Server: "]).start()

    # Méthode pour écouter les communications client
    def listening_client(self):
        # Réception du paquet contenant l'IP et le port réels
        packet = self.connexion.recv(1024).decode()
        packet = packet.split(" ")[1].split(":")
        self.start_server(packet)
        self._boucle_recv_send(self.connexion, self.socket_to_server, "Client: ")
        self._switch_server()

    # Méthode pour basculer vers un nouveau serveur
    def _switch_server(self):
        self.socket_to_server.close()
        self.socket_to_client.close()
        self.connexion.close()
        Thread(None, self.__init__, args=[self.server_ip, self.server_port, self.interface, self.packet_gestion]).start()

    # Méthode pour lancer l'hameçonnage (hooking)
    def _hook(self):
        fritm.spawn_and_hook((PATH + "/Dofus.exe"), 6555)
        self.httpd = fritm.start_proxy_server(None)

    # Boucle de réception et d'envoi de paquets
    def _boucle_recv_send(self, recv, send, source, packets=None):
        while packets != "":
            try:
                packets = recv.recv(1024)
                send.send(packets)
            except:
                break
            packets = packets.decode()
            # Traitement spécifique pour les paquets provenant du client
            if source == "Client: ":
                if packets[:5] == "GA001":
                    print(packets.split())
            for packet in packets.split("\x00"):
                Thread(None, self.interface.ongletsPackets.print_packet, args=[(source + packet)]).start()
                # Traitement spécifique pour les paquets provenant du serveur
                if source == "Server: ":
                    self.packet_gestion.server_packet(packet)
        recv.close()
        print("Connection closed with " + source)

# Point d'entrée principal du script
if __name__ == "__main__":
    MITM()
