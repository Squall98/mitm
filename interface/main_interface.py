import tkinter, threading
from tkinter import ttk
from interface.onglets.onglets_map import OngletsMap
from interface.onglets.onglets_packets import OngletsPackets
from interface.onglets.onglets_personnage import OngletsPersonnage
from interface.onglets.onglets_sorts import OngletsSorts
import time

app_running = True


class MainInterface(threading.Thread):

    def __init__(self):
        global app_running
        if app_running:
            try:
                threading.Thread(None, self.launch).start()
            except RuntimeError as e:
                print(f"Erreur lors du démarrage du thread: {e}")
        while True:
            time.sleep(1)
            if self.ongletsSorts:
                break

    def set_character(self, character):
        global app_running
        self.character = character
        self.ongletsMap.set_character(character)
        self.ongletsSorts.set_character(character)
        self.ongletsPersonnage.set_character(character)
        if app_running:
            try:
                threading.Thread(None, self.character_statue).start()
            except RuntimeError as e:
                print(f"Erreur lors du démarrage du thread: {e}")

    def character_statue(self):
        en_mouvement = tkinter.Label(self.main, bg="red", text="En mouvement")
        en_mouvement.place(relx=0.05, rely=0.05, relwidth=0.08, relheight=0.04)

        en_recolte = tkinter.Label(self.main, bg="red", text="En recolte")
        en_recolte.place(relx=0.05, rely=0.10, relwidth=0.08, relheight=0.04)

        en_combat = tkinter.Label(self.main, bg="red", text="En combat")
        en_combat.place(relx=0.05, rely=0.15, relwidth=0.08, relheight=0.04)
        while True:
            time.sleep(1)
            if self.character.deplacement.ismouving:
                en_mouvement.configure(bg="Green")
            else:
                en_mouvement.configure(bg="Red")
            if self.character.isharvest:
                en_recolte.configure(bg="Green")
            else:
                en_recolte.configure(bg="red")
            if self.character.isfighting:
                en_combat.configure(bg="Green")
            else:
                en_combat.configure(bg="red")

    def launch(self):
        self.main = tkinter.Tk()
        self.main.title("Squall-BBD")
        self.main.geometry('1200x900')
        self.create_notebook()
        self.main.mainloop()

    def create_notebook(self):
        self.onglets = tkinter.ttk.Notebook(self.main)
        self.onglets.pack()
        self.onglets.place(relx=0.15, rely=0.05, relwidth=0.83, relheight=0.83)

        self.ongletsPackets = OngletsPackets(self.onglets)
        self.ongletsPersonnage = OngletsPersonnage(self.onglets)
        self.ongletsMap = OngletsMap(self.onglets)
        self.ongletsSorts = OngletsSorts(self.onglets)

    def base_start(self, character):
        self.vita = tkinter.Label(self.main, bg="red", text=character.vie_actuelle + " / " + character.vie_max)
        self.vita.pack()
        self.vita.place(relx=0.20, rely=0.90, relwidth=0.08, relheight=0.08)

        self.energie = tkinter.Label(self.main, bg="yellow",
                                     text=character.ennergie_actuelle + " / " + character.ennergie_max)
        self.energie.pack()
        self.energie.place(relx=0.40, rely=0.90, relwidth=0.08, relheight=0.08)

        self.xp = tkinter.Label(self.main, bg="deep sky blue", text=character.xp_actuelle + " / " + character.xp_fin)
        self.xp.pack()
        self.xp.place(relx=0.60, rely=0.90, relwidth=0.1, relheight=0.08)

        self.kamas = tkinter.Label(self.main, bg="orange", text=character.kamas)
        self.kamas.pack()
        self.kamas.place(relx=0.80, rely=0.90, relwidth=0.08, relheight=0.08)


if __name__ == "__main__":
    try:
        app = MainInterface()
        # Insérez ici toute logique supplémentaire pour démarrer ou configurer l'application.
    finally:
        app_running = False  # Mettre à jour l'état lors de la fermeture de l'application.
        # Si vous avez conservé des références aux threads, vous pouvez les joindre ici pour vous assurer qu'ils terminent proprement.
        # Par exemple:
        # for thread in my_threads:
        #     thread.join()