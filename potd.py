import json

from discord import *

PotdDataFilePath = "potd.json"
contenderList = []
maxPoints = 1000000


class Contender:
	def __init__(self, user, name, pts):
		self.user = user
		self.username = name
		self.points = pts

	def __lt__(self, other):
		if (self.points != other.points):
			return self.points < other.points
		return False

	def __gt__(self, other):
		if (self.points != other.points):
			return self.points > other.points
		return False

	def updatePoints(self, gained):
		newPoints = min(self.points + gained, maxPoints)
		self.points = newPoints

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def updateContender(x):
	if isinstance(x, Contender):
		for i in range(len(contenderList)):
			if (int(contenderList[i].user) == int(x.user)):
				x.updatePoints(contenderList[i].points)
				del contenderList[i]
				break
		A = True
		for i in range(len(contenderList)):
			if (x > contenderList[i]):
				contenderList.insert(i, x)
				A = False
				break
		if (A):
			contenderList.append(x)
		save()


async def getContenderList(bot, message):
	e = Embed(title="POTD Leaderboard")
	for i in range(10):
		try:
			e.add_field(name=str(i + 1) + ". " + str(contenderList[i].username),
						value=str(contenderList[i].points) + " points", inline=False)
		except:
			break
	await message.channel.send(embed=e)


async def getContenderData(bot, message):
	name = message.mentions[0].id
	found = False
	for i in range(len(contenderList)):
		if (int(contenderList[i].user)==name):
			found = True
			await message.channel.send(contenderList[i].username + " has " + str(
				contenderList[i].points) + " points for POTD")
	if (not found):
		await message.channel.send(message.mentions[0].name + " has 0 points for POTD")


async def updateLeaderboard(bot, message):
		name = message.mentions[0].id
		nameToShow = message.mentions[0].name
		try:
			content = message.content[:message.content.index('pts')].strip()
		except:
			content = message.content.strip()
		score = min(int(content.split()[-1]), maxPoints)
		updateContender(Contender(name, nameToShow, score))

async def fixLeaderboard(bot, message):
		name = message.mentions[0].id
		nameToShow = message.mentions[0].name
		try:
			content = message.content[:message.content.index('pts')].strip()
		except:
			content = message.content.strip()
		score = min(int(content.split()[-1]), maxPoints)
		updateContender(Contender(name, nameToShow, -score))



# START IO
def encode_Contender(x):
	if isinstance(x, Contender):
		return {"user": (x.user), "username": (x.username), "pts": (x.points)}
	else:
		raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_Contender")


def decode_Contender(x):
	return Contender(x["user"], x["username"], x["pts"])


def save():
	with open(PotdDataFilePath, "w") as write_file:
		json.dump(contenderList, write_file, default=encode_Contender, sort_keys=False, indent=2)
# def load():
#	global contenderList
#	with open(PotdDataFilePath, "r") as read_file:
#		contenderList = json.load(read_file, object_hook=decode_Contender)
# END IO

# load()
