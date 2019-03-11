import datetime
import json

import discord
from discord import *

MuteDataFilePath = "mute.json"

muteList = []
class Muted:
	def __init__(self, user, when):
		self.user = user
		self.endOfMute = when
	
	def operator __lt__ (self, other):
		if(endOfMute != other.endOfMute):
			return endOfMute < other.endOfMute
		return self.user.id < other.user.id
	
	def operator __gt__ (self, other):
		if(endOfMute != other.endOfMute):
			return endOfMute > other.endOfMute
		return self.user.id > other.user.id
	
	def increase_mute_length(x, penalty):
		endOfMute = endOfMute + penalty;


def save():
	with open(MuteDataFilePath, "w") as write_file:
		json.dump(muteList, write_file)

