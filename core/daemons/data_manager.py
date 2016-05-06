# -*- coding: utf8 -*-

from threading import Thread
from time import sleep


class daemon_data(Thread):
    '''thread gérant toutes les données, leur réception et leur acheminement
        vers les threads qui en ont besoin.
    données en provenance de :
        - gant
        - switches (un triplet de touches (freq--, pause-play, freq++))
        - keys (simulation d'un clavier de piano, touches de 'a' à 'n')

    NOTES :
        - la lecture des touches entrées sur le clavier du laptop se fait dans
            le core (apparemment obligatoire... ?)

    '''

    def __init__(self, scr, core_ref, d_glove_ref, d_audio_ref):
        Thread.__init__(self)
        self.scr = scr
        self.core = core_ref
        self.d_glove = d_glove_ref
        self.d_audio = d_audio_ref
        self.core.logger.p_log('(DATA) init')

    def run(self):
        while 1:
            sleep(.01)
            try:
            # veille sur les switchs
                # switch1 sur {f2, f3, f4}
                if self.core.last_entry == 266:
                    self.scr.addstr(5, 170, 'son a--'+9*" ")
                if self.core.last_entry == 267:
                    self.scr.addstr(5, 170, 'son a pause/play')
                if self.core.last_entry == 268:
                    self.scr.addstr(5, 170, 'son a++'+9*" ")

            # veille sur le data_glove
                if self.d_glove.formated_data['loggingSample'] == 0:
                    self.d_glove.formated_data['loggingSample'] = "no socket data"
            except:
                self.core.erreurs = "erreur dans input_laptop"

    def get_data_glove(self, data_type):
        return self.data_glove[data_type]

    def get_data_switch(self, switch_number):
        return self.data_switch[switch_number]
