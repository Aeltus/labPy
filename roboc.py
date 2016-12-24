#!/usr/bin/python3.4
# -*-coding:Latin-1 -*

import os
import pickle
from classes.player import *
from classes.files import *

"""=====================================================================================================================
Initialisation du jeu
====================================================================================================================="""
poursuivre = 1

print("Bienvenue sur Roboc, le jeu de labyrinthe d�velopp� pour OC \n")

maps = os.listdir("dic/maps")

print("Quelle carte choisissez vous ?\n")
for (i, map) in enumerate(maps):
    print("{0}- {1}".format(i+1, map[0:-4]))

numMap = input("Entrez le numero du labyrinthe pour commencer � jouer : ")
"""=================================================================================================================="""

"""=====================================================================================================================
V�rification de l'existance d'une sauvegarde + demande si d�marrage sur sauvegarde ou nouvelle partie
====================================================================================================================="""
numMap = int(numMap)-1
print("Carte : {0}".format(maps[numMap][0:-4]))
response = "n"

if os.path.exists("dic/svg/"+maps[numMap]):
    response = input("Une sauvegarde pr�c�dente existe, remprendre la partie en cours ? y/n")
    response = str.lower(response)

if response == "y":
    origin = "dic/svg/"
else:
    origin = "dic/maps/"

"""=================================================================================================================="""

"""=====================================================================================================================
Consultation du fichier
+ creation du dictionnaire de la map
+ affichage � chaque tour de boucle, la boucle se finit quand le robot est sur l'arriv�e
====================================================================================================================="""
player = Player()

while True:
    win = False
    mapDictionnary = {}

    """ Si on part d'un fichier vierge, on cr�e un dictionnaire � partir de ce fichier """
    if origin == "dic/maps/":
        content = Files.fopen(origin+maps[numMap])
        x = 0
        y = 0
        for (i, symbol) in enumerate(content):
            localisation = (x, y)
            mapDictionnary[localisation] = symbol

            x += 1

            if symbol == "\n":
                y += 1
                x = 0

    """"Sinon, on r�cup�re le dictionnaire enregistr�"""
    else:
        with open(origin+maps[numMap], 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            mapDictionnary = mon_depickler.load()

    """On parcours le dictionnaire, pour en afficher chaque ligne"""
    contentLine = ""
    x = y = 0
    while True:
        location = (x, y)
        if location in mapDictionnary:
            contentLine = "{}{}".format(contentLine, mapDictionnary[location])

            if mapDictionnary[location] == "X":
                player.x = x
                player.y = y
            x += 1
        else:
            print(contentLine[0:-1])
            contentLine = ""
            y += 1
            x = 0
            location = (x, y)
            if location not in mapDictionnary:
                break


    """=============================================================================================================="""

    """=================================================================================================================
    Demande quoi faire
    + analyse la r�ponse
    + test si la route choisie est possible � suivre sans obstacles
    ================================================================================================================="""

    directive = input("Ou aller ? (n = nord, s = sud, e = est, o = ouest, q = quitter)")
    directive = "{0} ".format(directive)
    direction = str.lower(directive[0])
    vitesse = directive[1:-1]
    mur = False
    l = 0

    if direction == "q":
        break

    if direction == "n":

        while l < int(vitesse):

            l += 1
            location = (player.x, player.y-l)
            if mapDictionnary[location] == "O":
                mur = True
                break
            if mapDictionnary[location] == "U":
                win = True
                break

    if direction == "s":

        while l < int(vitesse):

            l += 1
            location = (player.x, player.y + l)
            if mapDictionnary[location] == "O":
                mur = True
                break
            if mapDictionnary[location] == "U":
                win = True
                break

    if direction == "e":

        while l < int(vitesse):

            l += 1
            location = (player.x + l, player.y)
            if mapDictionnary[location] == "O":
                mur = True
                break
            if mapDictionnary[location] == "U":
                win = True
                break

    if direction == "o":

        while l < int(vitesse):

            l += 1
            location = (player.x - l, player.y)
            if mapDictionnary[location] == "O":
                mur = True
                break
            if mapDictionnary[location] == "U":
                win = True
                break

    if mur:
        print("Vous ne pouvez suivre cette route, car un mur vous en emp�che")
    else:
        print("Le robot avance !!!")

        """=========================================================================================================="""

        """=============================================================================================================
        Si gagn� on supprime le fichier de sauvegarde et on sort de la boucle
        ============================================================================================================="""
        if win:
            os.remove(origin+maps[numMap])
            break
        """=========================================================================================================="""

        """=============================================================================================================
        Sinon, on met � jour le dictionnaire, on l'enregistre en sauvegarde et on repart pour un tour de boucle
        ============================================================================================================="""

        mapDictionnary[location] = "X"
        playerLocation = (player.x, player.y)
        mapDictionnary[playerLocation] = " "
        origin = "dic/svg/"

        with open(origin+maps[numMap], 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(mapDictionnary)
        """=========================================================================================================="""

if win:
    print("Vous avez gagn�\nMerci d'avoir jou� !!!")
else :
    print("A la prochaine fois !!!")