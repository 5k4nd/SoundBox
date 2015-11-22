# -*- coding: utf8 -*-

from threading import Thread
from input_scapy import daemon_glove
from output_graphic import daemon_curses
from data_manager import daemon_data
from time import sleep
import traceback

from curses import (
    endwin,
    BUTTON_CTRL,
    BUTTON_SHIFT,
    A_NORMAL,

)


class core(Thread):
    '''thread principal, gère tous les autres threads à savoir :
        - thread inputs
        - thread de calcul et gestion des données
        - thread outputs (graphique et audio)

        > contient la boucle infinie de capture de touche entrée au clavier.

    '''

    def __init__(self, SERVER_IP, SERVER_PORT, SCR):
        Thread.__init__(self)
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.scr = SCR
        self.last_entry = "none"
        self.erreurs = "pas d'erreurs pour le moment"


    def run(self):
        # on lance keyboard AVANT curses pour qu'ce dernier ait la main sur scr
        d_glove = daemon_glove()
        d_glove.start()
        self.d_data_manager = daemon_data(self.scr, core_ref=self)
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
            if 0 < current_entry < 256:  # si lettre connue, on la traite
                # on commence par le stocker
                # on remplit avec des blancs pour que ça fasse tjrs 5 " "
                self.last_entry = str(current_entry) +\
                    (5 - len(str(current_entry))) * " "

                if current_entry == ord('q'):
                    break


        # FIN DU PROGRAMME, ON NETTOIE TOUT
        d_glove.kill_daemon_data_network()
        d_glove._Thread__stop()
        self.d_data_manager._Thread__stop()
        self.d_curses._Thread__stop()
        endwin()  # restaure le terminal à son état d'origine
        traceback.print_exc()  # affiche exception si il y a
