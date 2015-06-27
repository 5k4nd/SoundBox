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

from curses import wrapper, start_color

from app import launch


if __name__ == '__main__':
    """ HowTo:
            go to SensorLog settings on your phone.
            set log data to 'socket'
            and get your IP and PORT (you can choose one or let it auto).
            csv sep must be ',' and 'fill' checked.
            recording rate over 50Hz is good
            then check what you want. for the moment, just ACC is (quite) well implemented.
            then 'Done', and start recording by pressing the play button.

            tip: you can check that your phone is sending packets over
                the network by launching 'nc phone_ip socket_port'
                in any linux terminal.
                Warning: nc and this script can't run together!
    """
    wrapper(launch, '10.42.0.63', 508) # phone_IP, socket_PORT

# toDo: 
#  * data_format
#  * clavier from tkinter
