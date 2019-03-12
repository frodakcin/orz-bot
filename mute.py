import datetime
from datetime import *
import json
import discord
from discord import *

muteList = []

class Muted:
	def __init__(self, user, when):
		self.user = user
		self.endOfMute = when
	
	def __lt__ (self, other):
		if(endOfMute != other.endOfMute):
			return endOfMute < other.endOfMute
		return self.user.id < other.user.id
	
	def __gt__ (self, other):
		if(endOfMute != other.endOfMute):
			return endOfMute > other.endOfMute
		return self.user.id > other.user.id
	
	def increase_mute_length(penalty):
		endOfMute = endOfMute + penalty;

async def mute(bot, message):
	try:
		content = message.content
		name = str(content[6:-3])
		amount = int(content[-2:-1])
		timeUnit = str(content[-1:])
		if(timeUnit=='s'):
			m = Muted(name, datetime.datetime.now() + timedelta(seconds=amount))
			load()
			muteList.append(encode_Muted(m))
			save()
			await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' second(s).')
		elif(timeUnit=='m'):
			m = Muted(name, datetime.datetime.now() + timedelta(minutes=amount))
			load()
			muteList.append(encode_Muted(m))
			save()
			await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' minute(s).')
		elif(timeUnit=='h'):
			m = Muted(name, datetime.datetime.now() + timedelta(hours=amount))
			load()
			muteList.append(encode_Muted(m))
			save()
			await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' hour(s).')
		elif(timeUnit=='d'):
			m = Muted(name, datetime.datetime.now() + timedelta(days=amount))
			load()
			muteList.append(encode_Muted(m))
			save()
			await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' day(s).')
		else:
			raise ValueError
	except:
		await bot.send_message(message.channel, 'Invalid format.')


#START IO
MuteDataFilePath = "mute.json"
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
		json.dump(muteList, write_file, default=encode_Muted, sort_keys=False, indent=2)
def load():
	global muteList
	with open(MuteDataFilePath, "r") as read_file:
		muteList = json.load(read_file, object_hook=decode_Muted)
#END IO


"""
load()
print (str(len(muteList)))
for x in muteList:
	print("user: {x.id}, " + str(x.endOfMute))
"""