#!/usr/bin/python2.7
# -*- coding: utf8 -*-

"""
SoundBox v2.
Licence GNU GPL v3.
    littleDad, 2015.
"""

from core import core
from curses import wrapper

def launch(scr):
    core(
        SERVER_IP='192.168.1.12',
        SERVER_PORT=508,
        SCR=scr,
        RECEPTION_MODE="ACC"  # données à recevoir
    ).start()

wrapper(launch)  # encapsulation pour curses

"""
ToDo :
    > finir de récupérer l'ancien
    > puis compléter l'UML

bugs:
    > curses se lance jamais vraiment si pyo ne démarre pas (typiquement, c'est le cas quand
        une instance de pyo est déjà en route dans un autre programme :p)

"""
