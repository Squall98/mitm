from character.job import recole, get_id
import tkinter
from tkinter import ttk


class OngletsMetier:
    def __init__(self, main_onglets):
        self.onglets_metier = ttk.Frame(main_onglets)
        self.onglets_metier.pack()
        main_onglets.add(self.onglets_metier, text='Metier')

        # Ajout d'un attribut pour suivre l'état de la récolte automatique
        self.recolte_auto_active = False

        # Ajout d'un bouton pour activer/désactiver la récolte automatique
        self.bouton_recolte = tkinter.Button(self.onglets_metier, text="Activer la récolte automatique",
                                             command=self.toggle_recolte_auto)
        self.bouton_recolte.pack()

    def toggle_recolte_auto(self):
        # Changer l'état de la récolte automatique
        self.recolte_auto_active = not self.recolte_auto_active

        # Mettre à jour le texte du bouton en fonction de l'état
        if self.recolte_auto_active:
            self.bouton_recolte.config(text="Désactiver la récolte automatique")
            self.recolter_ressource_ble()  # Lancer la récolte automatique
        else:
            self.bouton_recolte.config(text="Activer la récolte automatique")
            # Ici, vous devrez implémenter la logique pour arrêter la récolte automatique