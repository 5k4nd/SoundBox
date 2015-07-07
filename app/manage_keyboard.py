# -*- coding: utf8 -*-

class KeyboardServer:
    """manage key binding
    as always, should be unique... ToDo!
    """
    state = None # focus on menu or clavier

    def __init__(self):
        self.state = "menu"

