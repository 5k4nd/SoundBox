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
        SCR=scr
    ).start()

wrapper(launch)  # encapsulation pour curses

"""
ToDo :
    > finir de récupérer le manage_data.py et puis le reste


"""
