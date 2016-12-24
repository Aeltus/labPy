# -*-coding:Latin-1 -*

"""Fichier de configuration du jeu"""

class Conf():

    def __init__(self):

        self._emptyMaps = "dic/maps/"
        self._svgMaps = "dic/svg/"


    def _set_emptyMaps(self, route):
        self._emptyMaps = route
    def _get_emptyMaps(self):
        return self._emptyMaps
    emptyMaps = property(_get_emptyMaps, _set_emptyMaps)


    def _set_svgMaps(self, route):
        self._svgMaps = route
    def _get_svgMaps(self):
        return self._svgMaps
    svgMaps = property(_get_svgMaps, _set_svgMaps)

