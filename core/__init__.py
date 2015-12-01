# -*- coding: utf8 -*-

from daemons.input_scapy import daemon_glove
from daemons.output_graphic import daemon_curses
from daemons.output_audio import daemon_audio
from daemons.data_manager import daemon_data

from threading import Thread
from time import sleep
from sys import exc_info
import traceback
from logger_02 import LogFile
from pprint import pprint

from curses import (
    endwin,
    BUTTON_CTRL, BUTTON_SHIFT, KEY_LEFT, # pas nécessaire, suffit de noter les analogies en INT
    A_NORMAL,

)


class core(Thread):
    '''thread principal, gère tous les autres threads à savoir :
        - thread inputs
        - thread de calcul et gestion des données
        - thread outputs (graphique et audio)

        > contient la boucle infinie de capture de touche entrée au clavier.

    '''

    def __init__(self, SERVER_IP, SERVER_PORT, SCR, RECEPTION_MODE):
        Thread.__init__(self)
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.scr = SCR
        self.last_entry = " none"
        self.erreurs = "pas d'erreurs pour le moment"
        self.reception_mode = RECEPTION_MODE
        self.logger = LogFile('app.log')
        self.logger.initself()


    def run(self):
        self.logger.p_log('program started', newline=3)

        try:
            d_audio = daemon_audio(self.logger)
        except:
            self.logger.p_log('pyo start daemon: ', error=exc_info())

        d_glove = daemon_glove(
            core_ref=self,
            mode=self.reception_mode
        )
        d_glove.start()
        self.d_data_manager = daemon_data(
            self.scr,
            core_ref=self,
            d_glove_ref=d_glove,
            d_audio_ref=d_audio
        )
        self.d_data_manager.start()  # Thread-2 = OBSOLETE !
        self.d_curses = daemon_curses(
            self.scr,
            core_ref=self,
            d_glove_ref=d_glove
        )
        self.d_curses.start()  # Thread-3 = OBSOLETE !

        sleep(.01)  # wait, pour être sûr que les thread soient bien lancés
        self.d_curses.scr_init()

        # boucle de get_key
        while 1:
            sleep(0.1)
            self.scr.nodelay(1)  # rend getch() non-bloquant
            current_entry = self.scr.getch()
            if 0 < current_entry < 356:  # si lettre connue, on la traite
                # on commence par le stocker
                # on remplit avec des blancs pour que ça fasse tjrs 5 " "
                self.last_entry = current_entry

                if current_entry == 27:  # <échap>  # ord('q')
                    break
            else:
                if current_entry == KEY_LEFT:
                    self.last_entry = str(current_entry)


        # FIN DU PROGRAMME, ON NETTOIE TOUT. RANGER TOUT ÇA DANS DES MÉTHODES
        # PROPRES À CHAQUE THREAD. en gros, "chacun chez soi" serait + cool !
        #d_audio.server.stop()
        d_glove.kill_daemon_data_network()
        d_glove._Thread__stop()
        self.d_data_manager._Thread__stop()
        self.d_curses._Thread__stop()

        endwin()  # restaure le terminal à son état d'origine
        self.logger.p_log('program ends.')
        print "traceback:"
        traceback.print_exc()  # affiche exception si il y a
