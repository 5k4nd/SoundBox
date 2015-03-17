#!/usr/bin/python2
#! -*- coding: utf8 -*-
"""
SoundBox.
	Permet, après avoir configuré le client SensorLog en mode ACC uniquement,
		de jouer avec la fréquence brute (en Hz) ou en utilisant les gammes.
batoo, 2015.
----
toDo:
 - axe de lacet avec le HEAD
"""
import socket
import curses
from curses import wrapper
from pyo import *
import gammes

##CONSTANTS
hostIP = '192.168.0.16'
port = 50583

#across the stars (or, the programm)
class dia:
	children = {}
	server = Server()
	gamme = gammes.g3
	gamme2 = gammes.g4
	count = None


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

def sound_map_spectrum(y, x, data):
#spectre : environ 250-500Hz (le do est à 261.63)
#tenir l'iPhone sur la tranche (boutons de volume vers le ciel, écran à droite)
	dia.sound.mul = 1
	data += 2**2
	data **= 4
	data += 100
	dia.sound.freq = round(data)

	scr.addstr(y, x, str(round(data)))#str(dia.sound.freq))
	scr.refresh()



def getData(self):
# faire de cette fonction un pid en tâche de fond
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((hostIP, port))
	s.shutdown(socket.SHUT_WR)
	
	while 1: #implémenter des signaux plutôt que cette boucle crade
	    data = ( s.recv(1024) ).split(',')
	    if len(data) == 6:
		#accéléromètre (ACC)
			data = {
		    	'logTime': data[0],
			    'logSample': data[1],
			    'logTime_sinceReboot': data[2],
			    'xAxis': data[3],
				'yAxis': data[4],
				'zAxis': data[5]
			}
			scr.addstr(2, 5, 'logSample')
			scr.addstr(4, 5, data['logSample'])
			scr.addstr(2, 30, 'logTime_sinceReboot')
			scr.addstr(4, 30, data['logTime_sinceReboot'])

		#note utile : les axes prennent en compte... l'accélération (obvious!)
		#axe de roulis
			scr.addstr(8, 5, 'xAxis')
			xData = float(data['xAxis'])
			scr.addstr(10, 5, str(xData))
			#sound_map(12, 5, xData)

		#axe de tangage
			scr.addstr(8, 30, 'yAxis')
			yData = (float(data['yAxis']))
			scr.addstr(10, 30, str(yData))
			#sound_map(12, 30, yData)

		#axe de roulis ?
			scr.addstr(8, 55, 'zAxis')
			zData = float(data['zAxis'])
			scr.addstr(10, 55, str(zData))
			sound_map_spectrum(12, 55, zData)

			scr.refresh()

	s.close()




if __name__ == '__main__':
#ncurses config
	scr = curses.initscr()
	#curses.noecho() # turn off automatic echoing of keys to the screen
	#curses.cbreak() # react to keys instantly
	#scr.keypad(1) # map special keys as PageUp or key-left

	scr.border(0)

#pyo config
	dia.server.boot().start()
	dia.sound = Sine(0, 0, 0).out()

#main loop
	dia.count = 0
	wrapper(getData)
	scr.getch()

#ending
	#dia.server.stop()
	#curses.nocbreak(); scr.keypad(0); curses.echo() # reset terminal settings
	#curses.endwin()
