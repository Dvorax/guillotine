from guillotine.game import Guillotine
from guillotine.player import Human, Computer, BadComputer
from ai.config import random_config, DEFAULT_CONFIG
from random import seed

players = [
		Computer('Ash', random_config()), 
		BadComputer('Gary')#, 
		# Computer('Prof Oak')
]


seed('play')
a = Guillotine(players)
# print('Type a.play() to play')
a.play()
