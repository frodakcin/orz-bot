import datetime
from datetime import *
import json
import discord
from discord import *

import mute
from mute import Muted

MuteDataFilePath = "mute.json"

muteList = []

def encode_datetime(dt):
	if isinstance(dt, datetime):
		return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
	else:
		raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_datetime")
		
def encode_Muted(x):
	if isinstance(x, Muted):
		return {"user": (x.user), "when": encode_datetime(x.endOfMute)}
	else:
		raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_Muted")

def get_datetime(x):
	return datetime(x[0], x[1], x[2], x[3], x[4], x[5])

def decode_Muted(x):
	return Muted(x["user"], get_datetime(x["when"]))

def save():
	with open(MuteDataFilePath, "w") as write_file:
		json.dump(muteList, write_file, default=encode_Muted, sort_keys=True, indent=2)

def load():
	global muteList
	with open(MuteDataFilePath, "r") as read_file:
		muteList = json.load(read_file, object_hook=decode_Muted)
		print(len(muteList))

