import datetime
from datetime import *
import json
import discord
from discord import *

MuteDataFilePath = "mute.json"
ServerID = "516125324711297024"
MutedRoleName = "Muted"
muteList = []

def get_role(server_roles, target_name):
	for each in server_roles:
		if each.name == target_name:
			return each
	return None

class Muted:
	def __init__(self, user, name, when):
		self.user = user
		self.name = name
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

async def mute_success(bot, channel, mutedUsr, amo, TU, dur):
	username = mutedUsr.display_name
	for i in range(len(muteList)):
		if(muteList[i].user == mutedUsr):
			insertMuted(Muted(mutedUsr, mutedUsr.name, muteList.pop(i).endOfMute + dur))
			await bot.send_message(channel, '{usrnm} has been muted for {amount} more {TU}(s).'.format(usrnm=username, amount=str(amo), TU=TU))
			return
	insertMuted(Muted(mutedUsr, mutedUsr.name, datetime.now() + timedelta(hours=amount)))
	await bot.send_message(channel, '{usrnm} has been muted for {amount} {TU}(s).'.format(usrnm=username, amount=str(amo), TU=TU))
	await bot.add_roles(mutedUsr, get_role(bot.get_server(ServerID).roles, MutedRoleName))

async def mute(bot, message):
	if(("moderator" in [y.name.lower() for y in message.mentions[0].roles]
			or "admin" in [y.name.lower() for y in message.mentions[0].roles]
			or "moot-maestro" in [y.name.lower() for y in message.mentions[0].roles]
			or "orz bot" in [y.name.lower() for y in message.mentions[0].roles])
			and message.mentions[0].id != message.author.id):
		return
	content = (message.content[5:]).split()
	usr = message.mentions[0]
	name = message.mentions[0].id
	username = message.mentions[0].name
	amount = int(content[1][:-1])
	timeUnit = content[1][-1:]
	if(name==message.author.id and amount<0):
		await bot.send_message(message.channel, 'Nice try.')
		await bot.send_message(message.channel, "!mute <@" + message.author.id + "> " + str(-1*int(amount)) + timeUnit)
		return
	if(timeUnit=='s'):
		mute_success(bot, message.channel, usr, amount, "second", timedelta(seconds=amount))
	elif(timeUnit=='m'):
		mute_success(bot, message.channel, usr, amount, "minute", timedelta(minutes=amount))
	elif(timeUnit=='h'):
		mute_success(bot, message.channel, usr, amount, "hour", timedelta(hour=amount))
	else:
		await bot.send_message(message.channel, "Invalid Syntax!")
		raise ValueError(timeUnit + " is not a valid Time Unit.");

async def getMuteList(bot, message):
	e = Embed(title="Mute List")
	for i in range(len(muteList)):
		 e.add_field(name=muteList[i].name, value = Muted(muteList[i].user, muteList[i].name, muteList[i].endOfMute).toString(), inline=False)
	await bot.send_message(message.channel, embed=e)

async def updateMutes(bot):
	varLEN = len(muteList)
	for i in range(varLEN):
		try:
			if(muteList[i].endOfMute < datetime.today()):
				await bot.remove_roles(bot.get_server(ServerID).get_member(muteList[i].user), get_role(bot.get_server(ServerID).roles, MutedRoleName))
				muteList.pop(i)
				i-=1
				varLEN-=1
			else:
				break
		except:
			break
	save()


#START IO
def encode_datetime(dt):
	if isinstance(dt, datetime):
		return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
	else:
		raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_datetime")
def encode_Muted(x):
	if isinstance(x, Muted):
		return {"user": (x.user), "name": (x.name), "when": encode_datetime(x.endOfMute)}
	else:
		raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_Muted")
def get_datetime(x):
	return datetime(x[0], x[1], x[2], x[3], x[4], x[5])
def decode_Muted(x):
	return Muted(x["user"], x["name"], get_datetime(x["when"]))
def save():
	with open(MuteDataFilePath, "w") as write_file:
		json.dump(muteList, write_file, default=encode_Muted, sort_keys=False, indent=2)
def load():
	global muteList
	with open(MuteDataFilePath, "r") as read_file:
		muteList = json.load(read_file, object_hook=decode_Muted)
#END IO

load()
