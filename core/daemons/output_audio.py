# -*- coding: utf8 -*-

from pyo import *
### pyo documentation : http://ajaxsoundstudio.com/pyodoc/
from sys import exc_info
from time import sleep
import gammes

class daemon_audio:
    """serveur de son du module pyo.
    nécessite d'être un Thread (pyo ne le nécessite pas expréssement) pour
    gérer la réception des erreurs dans un run()

    Attributes:
      * ensemble de s_foo : des sons

    Methods:
      * sound_map_spectrum() -- joue selon l'orientation du gant
    """

    #def __init__(self, core_ref):
    def __init__(self, LOGGER):
        """create an unique instance of SoundServer.

        ToDo:
          * must be SINGLETON

        """

        self.logger = LOGGER
        self.server = Server()
        self.server.boot().start()
        #self.s_a = Sine(451, 0, 1).out()
        self.son1 = daemon_audio.Sound("do")
        self.son1.volume(1)
        self.logger.p_log('pyo Server initialized')
        
    def run(self):
        i=0
        while 1 & (i<200):
            sleep(.01)
            a = 42
            i += 1
            


    class Sound:
        # Sine(self, freq=1000, phase=0, mul=1, add=0)
        def __init__(self, NOTE, GAMME="g2"):
            Sine(
                freq = eval("gammes." + GAMME)[NOTE],
                mul = 0
            ).out()

        def volume(self, value):
            '''maybe this method could be filled with variations attribute or
                other nice things ?
            '''
            self.mul = value


# tests liés à l'audio
if __name__ == '__main__':
    exit(0)
    def start_server_try(server):
        '''cette fonction serait mieux en inline. ça existe en python ?'''
        try:
            server.boot().start()
        except:
            print "> pyo Server start error" + str(exc_info())

    #d_audio = daemon_audio()

    while 1:
        sleep(.01)
        s = Server()
        #start_server_try(s)
        s.boot().start()
        a=Sine(451,0,1).out()
        son1 = daemon_audio.Sound("do")
        son1.volume(1)
        