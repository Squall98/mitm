# Squall-BBD : Interface de Gestion pour Jeu

Squall-BBD est une application con�ue pour enrichir l'exp�rience de jeu en offrant une interface utilisateur avanc�e pour la gestion des personnages, des cartes, et des interactions r�seau. Ce projet, structur� autour d'une architecture modulaire, int�gre des fonctionnalit�s complexes et offre une interface r�active et intuitive.

## Caract�ristiques Principales

- **Gestion des Personnages** : Permet aux utilisateurs de visualiser et de g�rer les d�tails des personnages, y compris leurs statistiques, �quipements, et sorts, � travers une interface d�di�e.
- **Visualisation et Interaction avec la Carte** : Offre une vue interactive des cartes du jeu, permettant aux utilisateurs de naviguer dans diff�rentes zones et d'interagir avec les �l�ments du jeu.
- **Communication R�seau** : G�re les �changes de paquets r�seau pour synchroniser l'�tat du jeu avec le serveur, assurant une exp�rience de jeu fluide.
- **Optimisation des Performances** : Utilise des techniques d'optimisation pour minimiser la latence et garantir une exp�rience utilisateur r�active.

## Modules Cl�s

### Gestion des personnages (`character.py`, `onglets_personnage.py`)
- **Character** : G�re l'ensemble des informations li�es au personnage, permettant une manipulation d�taill�e de ses attributs.
- **OngletsPersonnage** : Fournit une interface graphique pour l'affichage et la gestion des informations du personnage.

### Gestion des cartes (`cell.py`, `map.py`, `onglets_map.py`)
- **Cell** : Repr�sente les cellules individuelles de la carte, avec des propri�t�s telles que l'accessibilit� et la ligne de vue.
- **Map** : Organise la carte dans son ensemble, g�rant le placement et les caract�ristiques des cellules.
- **OngletsMap** : Pr�sente la carte au joueur de mani�re interactive, permettant une navigation et une interaction ais�es.

### Communication r�seau (`packet_gestion.py`)
- **PacketGestion** : Traite les communications r�seau, interpr�tant les paquets re�us et envoyant des commandes au serveur selon les actions de l'utilisateur.

### Visualisation des sorts (`onglets_sorts.py`)
- **OngletsSorts** : Offre une vue d�taill�e des sorts disponibles pour le personnage, permettant aux utilisateurs de consulter et de g�rer leurs sorts.

## D�pendances

- **Tkinter** : Utilis� pour la cr�ation de l'interface utilisateur graphique.
- **Threading** : Permet de g�rer les t�ches en arri�re-plan, am�liorant la r�activit� de l'application.

## Installation et Utilisation

Cloner le d�p�t et installer les d�pendances n�cessaires � l'aide de pip. Lancer ensuite le script principal pour d�marrer l'application :

```bash
git clone https://github.com/Squall98/mitm/tree/master
cd Squall-BBD
pip install -r requirements.txt
python mitm.py


Contribution
Les contributions au projet sont les bienvenues. Pour contribuer, veuillez forker le d�p�t, cr�er une branche pour vos modifications, et soumettre une pull request.

Licence
Squall-BBD est distribu� sous la licence MIT. Veuillez consulter le fichier LICENSE pour plus de d�tails.
```
## Contribution
Les contributions au projet sont les bienvenues. Pour contribuer, veuillez forker le d�p�t, cr�er une branche pour vos modifications, et soumettre une pull request.

## Licence
Squall-BBD est distribu� sous la licence MIT. Veuillez consulter le fichier LICENSE pour plus de d�tails.