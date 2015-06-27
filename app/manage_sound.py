#! -*- coding: utf8 -*-

from pyo import *
import gammes
### pyo documentation : http://ajaxsoundstudio.com/pyodoc/


class SoundServer:
    """manages sounds, from womb (computer) to tomb (you!)

    Attributes:
      * sound: a sound
        > Sine(self, freq=1000, phase=0, mul=1, add=0)


    Methods:
      * sound_map_spectrum() -- joue selon l'orientation du gant
    """

    def __init__(self):
        """create an unique instance of SoundServer.

        ToDo:
          * must be SINGLETON

        """
        self.server = Server()
        self.server.boot().start()
        self.sound1 = Sine(451, 0, 0).out()


### pyo and sound mappings
    # lot of fun in this function. try new mappings!
    def sound_map(y, x, data):
        dia.sound.mul = 1
        if data == 0.0:
            scr.addstr(y, x, 'do')
            dia.sound.freq = dia.gamme['do']
        else:
            scr.addstr(y, x, 'sol')
            dia.sound.freq = dia.gamme['sol']
        dia.count += 1
        scr.addstr(2, 70, str(dia.count))
        scr.refresh()

    def sound_map_alter(y, x, data):
        dia.sound.mul = 1
        if data < -0.5:
            dia.sound.freq += 5
        elif data > 0.5:
            dia.sound.freq -= 5     
        scr.addstr(y, x, str(dia.sound.freq))
        scr.refresh()

    def sound_map_variations(self, data):
    #spectre : environ 250-500Hz (le do est à 261.63)
    #tenir l'iPhone sur la tranche (boutons de volume vers le ciel, écran à droite)
        self.sound1.mul = 1
        data += 2**2
        data **= 4
        data += 100
        self.sound1.freq = round(data)

        

