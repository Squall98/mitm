from character.job import recole, get_id
import tkinter
from tkinter import ttk


class OngletsMetier:

    def __init__(self, main_onglets):
        self.onglets_metier = ttk.Frame(main_onglets)
        self.onglets_metier.pack(expand=True, fill='both')
        main_onglets.add(self.onglets_metier, text='Métier')

        # Menu déroulant pour la sélection du métier
        self.selected_metier = tk.StringVar(self.onglets_metier)
        self.metiers = ['Boulanger', 'Forgeron', 'Alchimiste', 'Paysan']
        self.selected_metier.set(self.metiers[0])  # par défaut

        self.menu_metier = tk.OptionMenu(self.onglets_metier, self.selected_metier, *self.metiers)
        self.menu_metier.pack(pady=10)

        # Bouton pour activer/désactiver l'action du métier
        self.bouton_action_metier = tk.Button(self.onglets_metier, text="Activer action", command=self.toggle_action_metier)
        self.bouton_action_metier.pack(pady=10)

        # État de l'action du métier
        self.etat_action_metier = tk.Label(self.onglets_metier, text="Aucune action active", fg="red")
        self.etat_action_metier.pack(pady=10)

    def toggle_action_metier(self):
        # Ici, tu peux ajouter la logique pour activer ou désactiver l'action de métier
        pass

