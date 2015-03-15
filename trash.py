	f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
	a = Sine(mul=f).out()
	f.play()


	# MODULATION
	mod = Sine(freq=6, mul=50)
	a = Sine(freq=mod + 440, mul=0.1).out()



	wav = SquareTable()
	env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
	met = Metro(.125, 12).play()
	amp = TrigEnv(met, table=env, mul=.1)
	pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
	out = Osc(table=wav, freq=pit, mul=amp).out()