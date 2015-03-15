#!/usr/bin/python2
# -*- coding: utf8 -*-
"""
Doc de pyo : http://ajaxsoundstudio.com/pyodoc/

#formatage d'un son
	Sine(self, freq=1000, phase=0, mul=1, add=0)

"""
from pyo import *
import Tkinter as tk
from time import sleep
import gammes

class m:
	children = {}
	s = Server()
	gamme = gammes.g3
	gamme2 = gammes.g4

def newChild(name, server):
	child = os.fork()
	if child == 0:
		if name == 'basse':
			bass(server)
	else:
		m.children[name] = child
		print m.children


def endOfMusic():
	# kill All Children and stop the sound server
	for child in m.children.items():
		print 'on tue le child ' + str(child[0] + ' (' + str(child[1]) + ')')
		os.system('kill '+str(child[1]))
		m.s.stop()



def keypress(event):
	text.insert('end', '%s => freq: %s\n' % (event.char, a.freq))

	if event.keysym == 'Escape':
		m.s.stop()
		win1.destroy()
	x = event.char

	if x == "z":
		a.freq = m.gamme['dod'] #34.65
	elif x == "e":
		a.freq = m.gamme['red'] #38.89
	elif x == "t":
		a.freq = m.gamme['fad'] #46.25
	elif x == "y":
		a.freq = m.gamme['sold'] #51.91
	elif x == "u":
		a.freq = m.gamme['lad'] #58.27
	elif x == "q":
		a.freq = m.gamme['do'] #130.81
	elif x == "s":
		a.freq = m.gamme['re'] #146.83
	elif x == "d":
		a.freq = m.gamme['mi'] #164.81
	elif x == "f":
		a.freq = m.gamme['fa'] #174.61
	elif x == "g":
		a.freq = m.gamme['sol'] #196
	elif x == "h":
		a.freq = m.gamme['la'] #220
	elif x == "j":
		a.freq = m.gamme['si'] #246.94
	elif x == "k":
		a.freq = m.gamme2['do'] #246.94
	else:
		print "touche '%s' non attribuée" % x



def bass(server):
	m.s.start()
	mel = Sine(0, 0, 1).out()
	bass = Sine(0, 0, 1).out()
	while 1:
		print 'début boucle'
		bass.freq = 400
		print 'set bass on'
		bass.mul = 1
		sleep(.5)
		print 'set bass off'
		bass.mul = 0.0

		mel.freq = 500
		print 'set mel on'
		mel.mul = 1
		sleep(.5)
		print 'set mel off'
		mel.mul = 0.0
	#os._exit(0)

def getFreq(noteFreq): #en entrée, choppe l'objet
	return noteFreq[1] # retourne le 2nd element du tuple

def delDiese(gamme):
	#del gamme['dod'], gamme['red'], gamme['fad'], gamme['sold'], gamme['lad']
	return gamme

def playGamme(gamme): # gammes.g2
	gamme = delDiese(gamme) # facultatif !
	for note, freq in sorted(gamme.items(), key=getFreq):
		#print "elif x == \""+liste[i]+"\":\n\ta.freq = "+str(freq)
		son.freq = freq
		sleep(1)

def keyAttribute():
	# fonction pour faciliter l'attribution de touches
	return None

def rootdef():
	if event.keysym == 'Escape':
		m.s.stop()
		win1.destroy()


if __name__ == '__main__':
	win1 = tk.Tk()
	win1.geometry('600x400')
	text = tk.Text(win1, background='black', foreground='white', font=('Comic Sans MS', 12))
	text.pack()
	
	m.s.boot().start()

#	f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
#	a = Sine(mul=f).out()
#	f.play()
	
#	playGamme(gammes.g2)

#	newChild('basse', m.s)	
#	newChild('melodie', s)

	a = Sine(451, 0, 1).out()
	win1.bind_all('<Key>', keypress)
	win1.mainloop()

	#root = Tk()
	#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	#root.overrideredirect(1)
	#root.geometry("%dx%d+0+0" % (w, h))
	#root.focus_set() # <-- move focus to this widget
	#root.bind_all("<Key>", rootdef)
	#root.mainloop()


	#fen1 = Tk()
	#tex1 = Label(fen1, text='Bonjour tout le monde !', fg='red')
	#tex1.pack()
	#bou1 = Button(fen1, text='Quitter', command = fen1.destroy)
	#bou1.pack()
	#fen1.mainloop()

	endOfMusic()