# -*- coding: utf8 -*-

from pyo import *
### pyo documentation : http://ajaxsoundstudio.com/pyodoc/
from sys import exc_info

class daemon_audio:
    """serveur de son du module pyo.
    nécessite d'être un Thread (pyo ne le nécessite pas expréssement) pour
    gérer la réception des erreurs dans un run()

    Attributes:
      * ensemble de s_foo : des sons

    Methods:
      * sound_map_spectrum() -- joue selon l'orientation du gant
    """

    def __init__(self, core_ref):
        """create an unique instance of SoundServer.

        ToDo:
          * must be SINGLETON

        """
        def start_server_try(self, core_ref):
            try:
                self.boot().start()
            except:
                core_ref.erreurs = "> pyo Server start error" + str(exc_info())
        self.core = core_ref
        self.server = Server()
        self.server.start_server_try(self.core)
        # Sine(self, freq=1000, phase=0, mul=1, add=0)
        self.s_a = Sine(451, 0, 0).out()
        #self.gamme = gammes.g3

    