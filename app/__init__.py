# -*- coding: utf8 -*-

from time import sleep
from manage_data import DataServer, DataBoard
from manage_sound import SoundServer
#from manage_keyboard import KeyboardServer

# imports dupliqués... alternative possible, ou pas ?
import socket
from pyo import *


### MENU ###
def erase_menu(stdscr, menu_y):
    "Clear the space where the menu resides"
    stdscr.move(menu_y, 0)
    stdscr.clrtoeol()
    stdscr.move(menu_y+1, 0)
    stdscr.clrtoeol()

def display_menu(stdscr, menu_y):
    "Display the menu of possible keystroke commands"
    erase_menu(stdscr, menu_y)
    stdscr.addstr(menu_y+1, 4,
                  'phoneIP: %s | port: %s' % ('fake_IP', 'fake'))
                    #in the future: remove fake_IP when DataServer is Singleton and has get methods
    stdscr.addstr(menu_y+2, 4,
                  'P)lay / S)top sound ; Q)uit')
    stdscr.addstr(menu_y+3, 4,
                  'Enter) or [space] to switch focus')


def main_keyloop(stdscr, data, sound):
    # Clear the screen and display the menu
    stdscr.clear()
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    menu_y = (stdscr_y-3)-1
    display_menu(stdscr, menu_y)

    # Allocate a subwindow for databoard and create the board object
    subwin = stdscr.subwin(stdscr_y-3, stdscr_x, 0, 0) # (line, column, y_begin, x_begin)
    board = DataBoard(subwin)

    # Main loop:
    while (1):
        c = stdscr.getch() # Get a keystroke
        stdscr.refresh()
        # Activate nodelay mode; getch() will return -1 ;
        # if no keystroke is available, instead of waiting.
        stdscr.nodelay(1)
        if 0<c<256:
            c = chr(abs(c)) # abs for the -1
            if c in 'Pp':
            # launch receiving data and sound_binding with this data
                board.set_screen('ACC')
                while (1):
                    c = stdscr.getch()
                    c = chr(abs(c))
                    if c in 'Ss':
                        sound.sound1.mul = 0
                        break
                    elif data.data_format(): # if data isn't corrupted
                        #board.update_screen('ALL', 'accelerometeraccelerationZ')
                        sound.sound_map_variations(data.formated_data['accelerometeraccelerationZ'])
                        stdscr.addstr(20, 55, str(data.formated_data['accelerometeraccelerationZ']))

                    sleep(.01)

            elif c in 'Qq':
                break

            elif c == curses.KEY_UP: print 'switch screens ??'
            elif c in ' \n':
                erase_menu(stdscr, menu_y)
                stdscr.addstr(menu_y, 6, 'Je suis un nouveau texte de nouveau'
                              'menu. Switch de screen ?')
                display_menu(stdscr, menu_y)
                
            else:
                # Ignore incorrect keys
                pass
        else:
            pass
    stdscr.nodelay(0)


def launch(stdscr, HOSTIP, PORT):
# starting threads for data and sound
    data = DataServer(HOSTIP, PORT)
    sound = SoundServer() #remove this in mainloop, and shutdown too
    
# enter the main loop -- key binding
    main_keyloop(stdscr, data, sound)

# exit the program properly
    data.sock.shutdown(socket.SHUT_WR)
    sound.server.stop()