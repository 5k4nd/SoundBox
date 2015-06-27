#!/usr/bin/python2.7
# -*- coding: utf8 -*-
"""
SoundBox:
  Permet, après avoir configuré le client SensorLog sur votre smartphone
  de jouer avec la fréquence brute (en Hz) ou en utilisant les gammes.
  Enjoy!
littleDad, 2015.
"""

################################
# axes:
#  * roll: roulis
#  * pitch: tangage
#  * yaw: lacet
####################################################################################

############
# NOTES:
#   * in curses, coordinates are ALWAYS (y,x) and NOT (x,y)
#
#
########################

from curses import wrapper

from app import launch


if __name__ == '__main__':
    wrapper(launch, '10.42.0.63', 508)

# toDo: 
#  * faire une méthode de formatage de données dans DataServer et l'appeler dans keyloop
#      dans cette méthode, faire en sorte d'écarter les valeurs aberrantes lifting_data()
#  * finir de vider les vieux main.py