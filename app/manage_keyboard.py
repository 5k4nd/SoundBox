# -*- coding: utf8 -*-

import gammes

class KeyboardServer:
    """manage key binding
    as always, should be unique... ToDo!

    """
    state = None # focus on menu or clavier

    L1 = ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    L2 = ['q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm']
    L3 = ['w', 'x', 'c', 'v', 'b', 'n']


    def bind_key_note(self, lettre):
        """bind the passed letter with a note from the gamme set in the current keyboard config"""
        
        if lettre in self.L1:
            association = dict(zip(self.L1, gammes.GAMME_SCHEME))
            note = association.get(lettre, "do")
            return note+' (g2)', gammes.g2[note]
        elif lettre in self.L2:
            association = dict(zip(self.L2, gammes.GAMME_SCHEME))
            note = association.get(lettre, "do")
            return note+' (g3)', gammes.g3[note]
        else: # on suppose que lettre in L3 le temps des tests
            association = dict(zip(self.L3, gammes.GAMME_SCHEME))
            note = association.get(lettre, "do")
            return note+' (g4)', gammes.g4[note]
        
        #full_gamme = gamme1.update(gamme2)
        #full_gamme.get(lettre, "do") #do is default note
        #return full_gamme




    def __init__(self):
        self.state = "menu"

