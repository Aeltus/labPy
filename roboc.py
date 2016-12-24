#!/usr/bin/python3.4
# -*-coding:Latin-1 -*

"""Controlleur principal faisant appel aux diff�rentes m�thodes
et attributs des classes n�cessaires au d�roulement du jeu"""

import os
from lib.player import *
from lib.map import Map
from conf.conf import Conf

"""=====================================================================================================================
Initialisation du jeu
====================================================================================================================="""
while True:
    data = Map()
    config = Conf()
    print("Bienvenue sur Roboc, le jeu de labyrinthe d�velopp� pour OC \n")

    maps = os.listdir(config.emptyMaps)

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

    if os.path.exists(config.svgMaps+maps[numMap]):
        response = str.lower(input("Une sauvegarde pr�c�dente existe, remprendre la partie en cours ? y/n "))

    if response == "y":
        origin = config.svgMaps
    else:
        origin = config.emptyMaps

    """=================================================================================================================="""

    """=====================================================================================================================
    Consultation du fichier
    + creation du dictionnaire de la map
    + affichage � chaque tour de boucle, la boucle se finit quand le robot est sur l'arriv�e
    ====================================================================================================================="""
    player = Player()

    while True:

        """ Si on part d'un fichier vierge, on cr�e un dictionnaire � partir de ce fichier """
        if origin == config.emptyMaps:
            data.creator(origin, maps[numMap])

            """"Sinon, on r�cup�re le dictionnaire enregistr�"""
        else:
            data.recuperator(origin, maps[numMap])

        """On parcours le dictionnaire, pour en afficher chaque ligne"""
        data.display(player)


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


        mapDictionnary = data.dic.copy()
        if direction == "q":
            break

        testMouvement = data.mouvement_try(direction, vitesse, player)

        if testMouvement[0]:
            print("Vous ne pouvez suivre cette route, car un mur vous en emp�che")
        else:
            print("Le robot avance !!!")

            """=========================================================================================================="""

            """=============================================================================================================
            Si gagn� on supprime le fichier de sauvegarde et on sort de la boucle
            ============================================================================================================="""
            if testMouvement[1]:
                os.remove(origin+maps[numMap])
                break
            """=========================================================================================================="""

            """=============================================================================================================
            Sinon, on met � jour le dictionnaire, on l'enregistre en sauvegarde et on repart pour un tour de boucle
            ============================================================================================================="""

            data.dic[testMouvement[2]] = "X"
            playerLocation = (player.x, player.y)
            data.dic[playerLocation] = " "
            origin = config.svgMaps

            data.saver(origin, maps[numMap])
            """=========================================================================================================="""

    if testMouvement[1]:
        print("Vous avez gagn�\nMerci d'avoir jou� !!!")
        response = str.lower(input("Voulez vous rejouer ? (y/n) "))
        if response == "n":
            break
    else:
        print("A la prochaine fois !!!")
        break