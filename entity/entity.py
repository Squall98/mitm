class Entity():

    def __init__(self, type_, cell=0, **kwargs):
        self.type = type_  # Type de l'entité (par exemple, joueur, monstre, PNJ, etc.)
        self.cell = cell  # La cellule sur laquelle l'entité se trouve
        self.isMainCharacter = False  # Booléen pour indiquer si cette entité est le personnage principal du joueur
        self.__dict__.update(kwargs)  # Mise à jour de l'instance avec des attributs supplémentaires fournis via kwargs

