import datetime
from datetime import timedelta
import json
import discord
from discord import *

MuteDataFilePath = "mute.json"

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

"""
load()
print (str(len(muteList)))
for x in muteList:
	print("user: {x.id}, " + str(x.endOfMute))
"""