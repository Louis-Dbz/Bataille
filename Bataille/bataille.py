from random import *
from PIL import *
import tkinter as tk
import string
import csv

# /******   Lecture du fichier csv qui contient le nom des cartes   ******\
# |******                 Création d'une liste cartes               ******|
# |****** 2 fichiers de cartes: - un à 54 carte: "cartes_54.csv"    ******|
# \******                       - un à 12 carte: "experimental.csv" ******/

cartes = []
fichier = open("experimental.csv", "rt")
lecteurCSV = csv.reader(fichier,delimiter=",",quotechar="r")
for ligne in lecteurCSV:
    cartes.append(ligne)
fichier.close()

def melange():

    """
    Fonction qui mélange la liste cartes
    Revoie 2 listes a, b
    """

    a = sample(cartes, int(len(cartes)/2))
    b = []
    for el in cartes:
        if el not in a:
            b.append(el)
    return a, b

m1, m2 = melange() # Création des mains, m1 et m2

mem = [0] # /** Liste qui répertorie les batailles avec des 1, autrement 0 **\
          # |**    Permet d'effecuter la bataille de manière graphique     **|
          # \**            Premier élément pour éviter un bug              **/

def sequence(m1 = m1, m2 = m2, c1 = [], c2 = []):

    """
    Fonction principale permettant de jouer un coup

    Paramètres
    ----------
    m1 : liste
        La main du premier joueur, par défaut m1
    m2 : liste
        La main du second joueur, par défaut m2
    c1 : liste
        Le tas du premier joueur, ne compte pas dans le décompte de ses cartes
    c2 : liste
        Le tas du second joueur, ne compte pas dans le décompte de ses cartes
    """

    if len(m1) != 0 and len(m2) != 0: # Vérifie que pour jouer un coup, les deux joueurs ont des cartes
        c1.append(m1.pop(0)) # Ajoute au tas la carte enlevé de la main
        c2.append(m2.pop(0))
    v1, v2 = c1[len(c1)-1], c2[len(c2)-1] # v1, v2 sont les cartes du dessus du tas

    if v1[0] == v2[0]: # Bataille
        if len(m1) == 0 and len(m2) == 0: # Si les deux joueur n'ont plus de cartes, Égalité
            Texte["text"] = "Égalité"
            return
        if mem[len(mem)-1] == 1:
            mem.append(0) # Même si bataille, on ajoute 0 à la liste mémoire car cette carte est face cachée
        else:
            mem.append(1) # Bataille, on ajoute 1 à la liste mémoire

    if len(m2) == 0: # On test à chaque manche si le joueur 2 a perdu
        majCarte(v1, v2, len(c1), len(c2)) # Appel de fonction d'affichage des cartes
        Texte["text"] = "Le joueur 1 gagne" # Modification texte Texte graphique
        return

    if len(m1) == 0: # On test à chaque manche si le joueur 1 a perdu
        majCarte(v1, v2, len(c1), len(c2)) # Appel de fonction d'affichage des cartes
        Texte["text"] = "Le joueur 2 gagne" # Modification texte Texte graphique
        return

    if v1[0] > v2[0]: # Le premier joueur remporte la manche
        mem.append(0) # Pas de bataille, on ajoute 0 à la liste mémoire
        while c1 != []: # Vide les tas dans les mains
            m1.append(c1.pop(0))
        while c2 != []:
            m1.append(c2.pop(0))

    if v1[0] < v2[0]: # Le second joueur remporte la manche
        mem.append(0) # Pas de bataille, on ajoute 0 à la liste mémoire
        while c2 != []: # Vide les tas dans les mains
            m2.append(c2.pop(0))
        while c1 != []:
            m2.append(c1.pop(0))

    if mem[len(mem)-2] == 1 and len(mem) >= 2: # S'il y a eu une bataille le tour précédent, alors carte face cachée
        majCarte("img/back.gif", "img/back.gif", len(c1), len(c2))
    else:
        majCarte(v1, v2, len(c1), len(c2))

    return

def majCarte(v1, v2, c1, c2, m1 = m1, m2 = m2):

    """
    Fonction qui modifie l'affichage tkinter

    Paramètres
    ----------
    v1, v2 : listes
        exemple : - [puissance carte, couleur carte]
                  - ["7","h"] 7 de coeur
        Les cartes du dessus du tas
    c1 : liste
        Le tas du premier joueur, ne compte pas dans le décompte de ses cartes
    c2 : liste
        Le tas du second joueur, ne compte pas dans le décompte de ses cartes
    m1 : liste
        La main du premier joueur, par défaut m1
    m2 : liste
        La main du second joueur, par défaut m2
    """

    nbrM1["text"] = str(len(m1)) # Texte qui affiche le nombre restant de carte dans les mains des joueurs
    nbrM2["text"] = str(len(m2))

    if len(m1) == 0: # Si le joueur 1 perd, carte du perdant s'affiche
        img1.config(file = "img/None.gif")
        return

    if len(m2) == 0: # Si le joueur 2 perd, carte du perdant s'affiche
        img2.config(file = "img/None.gif")
        return

    if v1 != "img/back.gif": # Si la carte n'est pas face cachée
        # Voir le fichier img pour mieux comprendre d'après l'exemple de v1 ci-dessus
        img1.config(file = "img/" + str(v1[0]) + str(v1[1]) + ".gif")
        img2.config(file = "img/" + str(v2[0]) + str(v2[1]) + ".gif")
    else: # Sinon carte face cachée
        img1.config(file = "img/back.gif")
        img2.config(file = "img/back.gif")

    return

racine = tk.Tk() # Implémentation de tkinter, en tant que racine
Quitter = tk.Button(racine, text="Quitter", command = racine.quit)
Quitter.place(relx = 0.08, rely = 0.85)
Jouer = tk.Button(racine, text="Jouer", command = sequence)
Jouer.place(relx = 0.42, rely = 0.1)

img1 = tk.PhotoImage(file="img/15Joker1.gif") # Carte du joueur 1
label1 = tk.Label(racine, image=img1)
label1.place(relx = 0.08, rely = 0.5) # Positionnement, relatif
img2 = tk.PhotoImage(file="img/15Joker2.gif") # Carte du joueur 2
label2 = tk.Label(racine, image = img2)
label2.place(relx = 0.7, rely = 0.5)

Texte = tk.Label(racine, text = "Jouez")
Texte.place(relx = 0.08, rely = 0.1)

nbrM1 = tk.Label(racine, text = str(len(m1))) # Nombre de carte du joueur 1 textuel
nbrM1.place(relx = 0.08, rely = 0.3)
nbrM2 = tk.Label(racine, text = str(len(m2))) # Nombre de carte du joueur 2 textuel
nbrM2.place(relx = 0.7, rely = 0.3)

racine.title('Bataille')
racine.geometry("325x325") # Fenêtre de 325 par 325
racine.mainloop() # Boucle d'affichage tkinter