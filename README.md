# Squall-BBD : Interface de Gestion pour Jeu

Squall-BBD est une application conçue pour enrichir l'expérience de jeu en offrant une interface utilisateur avancée pour la gestion des personnages, des cartes, et des interactions réseau. Ce projet, structuré autour d'une architecture modulaire, intègre des fonctionnalités complexes et offre une interface réactive et intuitive.

## Caractéristiques Principales

- **Gestion des Personnages** : Permet aux utilisateurs de visualiser et de gérer les détails des personnages, y compris leurs statistiques, équipements, et sorts, à travers une interface dédiée.
- **Visualisation et Interaction avec la Carte** : Offre une vue interactive des cartes du jeu, permettant aux utilisateurs de naviguer dans différentes zones et d'interagir avec les éléments du jeu.
- **Communication Réseau** : Gère les échanges de paquets réseau pour synchroniser l'état du jeu avec le serveur, assurant une expérience de jeu fluide.
- **Optimisation des Performances** : Utilise des techniques d'optimisation pour minimiser la latence et garantir une expérience utilisateur réactive.

## Modules Clés

### Gestion des personnages (`character.py`, `onglets_personnage.py`)
- **Character** : Gère l'ensemble des informations liées au personnage, permettant une manipulation détaillée de ses attributs.
- **OngletsPersonnage** : Fournit une interface graphique pour l'affichage et la gestion des informations du personnage.

### Gestion des cartes (`cell.py`, `map.py`, `onglets_map.py`)
- **Cell** : Représente les cellules individuelles de la carte, avec des propriétés telles que l'accessibilité et la ligne de vue.
- **Map** : Organise la carte dans son ensemble, gérant le placement et les caractéristiques des cellules.
- **OngletsMap** : Présente la carte au joueur de manière interactive, permettant une navigation et une interaction aisées.

### Communication réseau (`packet_gestion.py`)
- **PacketGestion** : Traite les communications réseau, interprétant les paquets reçus et envoyant des commandes au serveur selon les actions de l'utilisateur.

### Visualisation des sorts (`onglets_sorts.py`)
- **OngletsSorts** : Offre une vue détaillée des sorts disponibles pour le personnage, permettant aux utilisateurs de consulter et de gérer leurs sorts.

## Dépendances

- **Tkinter** : Utilisé pour la création de l'interface utilisateur graphique.
- **Threading** : Permet de gérer les tâches en arrière-plan, améliorant la réactivité de l'application.

## Installation et Utilisation

Cloner le dépôt et installer les dépendances nécessaires à l'aide de pip. Lancer ensuite le script principal pour démarrer l'application :

```bash
git clone https://github.com/Squall98/mitm/tree/master
cd Squall-BBD
pip install -r requirements.txt
python mitm.py


Contribution
Les contributions au projet sont les bienvenues. Pour contribuer, veuillez forker le dépôt, créer une branche pour vos modifications, et soumettre une pull request.

Licence
Squall-BBD est distribué sous la licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.
```
## Contribution
Les contributions au projet sont les bienvenues. Pour contribuer, veuillez forker le dépôt, créer une branche pour vos modifications, et soumettre une pull request.

## Licence
Squall-BBD est distribué sous la licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.