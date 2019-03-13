import datetime
from datetime import *
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
		if(self.endOfMute != other.endOfMute):
			return self.endOfMute < other.endOfMute
		return self.user.id < other.user.id

	def __gt__ (self, other):
		if(self.endOfMute != other.endOfMute):
			return self.endOfMute > other.endOfMute
		return self.user.id > other.user.id

	def increase_mute_length(self, penalty):
		self.endOfMute += penalty;

	def toJSON(self):
		return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)
	
	def toString(self):
		if(self.endOfMute.day == datetime.today().day):
			return self.endOfMute.strftime("Today at %H:%M:%S")
		return self.endOfMute.strftime("%B %d, %Y at %H:%M:%S")
	
def insertMuted(x):
	if isinstance(x, Muted):
		A = True
		for i in range(len(muteList)):
			if(x < muteList[i]):
				muteList.insert(i, x)
				A = False
				break
		if(A):
			muteList.append(x)
		save()
	else:
		raise TypeError("You can only insert Muted objects!")


async def mute(bot, message):
	content = (message.content[5:]).split()
	name = content[0]
	amount = int(content[1][:-1])
	timeUnit = content[1][-1:]
	if(timeUnit=='s'):
		for i in range(len(muteList)):
			if(muteList[i].user == name):
				insertMuted(Muted(name, muteList.pop(i).endOfMute + timedelta(seconds=amount)))
				await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more second(s).')
				return
		insertMuted(Muted(name, datetime.now() + timedelta(seconds=amount)))
		await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' second(s).')
		
	if(timeUnit=='m'):
		for i in range(len(muteList)):
			if(muteList[i].user == name):
				insertMuted(Muted(name, muteList.pop(i).endOfMute + timedelta(minutes=amount)))
				await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more minute(s).')
				return
		insertMuted(Muted(name, datetime.now() + timedelta(minutes=amount)))
		await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' minute(s).')
		
	if(timeUnit=='h'):
		for i in range(len(muteList)):
			if(muteList[i].user == name):
				insertMuted(Muted(name, muteList.pop(i).endOfMute + timedelta(hours=amount)))
				await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more hour(s).')
				return
		insertMuted(Muted(name, datetime.now() + timedelta(hours=amount)))
		await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' hour(s).')
		
	else:
		await bot.send_message(message.channel, "Invalid Syntax!")
		raise ValueError(timeUnit + " is not a valid Time Unit.");
		
async def getMuteList(bot, message):
	e = Embed(title="Mute List", description='This gives the time when users will be unmuted.')
	for i in muteList:
		 e.add_field(name=i.user, value = Muted(i.user, i.endOfMute).toString(), inline=False)
	await bot.send_message(message.channel, embed=e)
	
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
		
load()
