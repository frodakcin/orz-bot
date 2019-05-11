import discord
from discord import *
import requests
import asyncio
from mute import *
from eight_ball import *
from geniosity import *
import censor
from potd import *
import time as rateLimitCounter

prefix = '!'
potdStatusChannelID = '518297095099121665'
token =  # remove when upload



class MyClient(discord.Client):


	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		raw = open(PotdDataFilePath, "w")
		raw.write("[\n]")
		raw.close()
		first = ""
		second = "-"
		beforeTag = ""
		while(second!=first):
			first = second
			messages = json.loads(
				requests.get("https://discordapp.com/api/v6/channels/" + potdStatusChannelID + "/messages?limit=100"+beforeTag,
							 headers={"authorization": token}).text)
			for i in messages:
				message = i['content']
				second = i['id']
				name = i['mentions'][0]['id']
				nameToShow = i['mentions'][0]['username']
				if ('pts' in message):
					content = message[:message.index('pts')].strip()
					score = min(int(content.split()[-1]), maxPoints)
				elif('AC' in message):
					score=100
				elif('WA' in message or 'TLE' in message or 'MLE' in message or 'CE' in message):
					score=0
				else:
					content = message.strip()
					score = min(int(content.split()[-1]), maxPoints)
				if (score < 0):
					score = 0
				updateContender(Contender(name, nameToShow, score))
				beforeTag = "&before=" + second
			rateLimitCounter.sleep(1) #rate-limiting
		print("Finished setting up POTD Leaderboard...")

		await self.change_presence(
			game=discord.Game(name="Tmw orz", url="https://codeforces.com/profile/tmwilliamlin168", type=0),
			status=Status.online, afk=False)

	async def on_message(self, message):
		if(message.author.id=="367469002374774786"): #imax pat
			await react_headpat(self, message)
		content = message.content

#################################################################
		if "twice sucks" in message.content.lower() and not ("moderator" in [y.name.lower() for y in message.author.roles]
														or "admin" in [y.name.lower() for y in message.author.roles]
														or "moot-maestro" in [y.name.lower() for y in message.author.roles]
														or "orz bot" in [y.name.lower() for y in message.author.roles]):
			await self.send_message(message.channel, "!mute <@" + message.author.id + "> 2015h")
			return
#################################################################

		if censor.enabled:
			if await censor.isCensored(content.lower()):
				print("Message \"" + content + "\" from user " + message.author.name + " has been deleted.")
				await self.delete_message(message)
				return
		if message.channel.id == potdStatusChannelID:
			await react_geniosity(self, message)
			await updateLeaderboard(self, message)

		if content.startswith(prefix):
			bot_command = True
			content = content[len(prefix):]
			if content.lower().startswith('mute ') and ("moderator" in [y.name.lower() for y in message.author.roles]
														or "admin" in [y.name.lower() for y in message.author.roles]
														or "moot-maestro" in [y.name.lower() for y in message.author.roles]
														or "orz bot" in [y.name.lower() for y in message.author.roles]
														or message.author.id == message.mentions[0].id):
				await mute(self, message)
			elif content.lower().startswith("mutelist"):
				await getMuteList(self, message)
			elif content.startswith('echo '):
				await self.send_message(message.channel, content[5:])
			elif content.startswith('8ball'):
				await make_prediction(self, message)
			elif content.lower().startswith('geniosity'):
				await print_geniosity(self, message)
			elif content.lower().startswith('leaderboard'):
				await getContenderList(self, message)
			elif content.lower().startswith('points'):
				await getContenderData(self, message)
			elif content.startswith("censor "):
				if censor.enabled:
					await censor.censor_command(self, message.channel, content[7:])
		else:
			if 'tmw' in content.lower():
				await react_tmw(self, message)
			if 'geniosity' in content.lower():
				await react_geniosity(self, message)
			if 'juicy' in content.lower():
				await react_juicy(self, message)
			if 'wtmoo' in content.lower():
				await react_wtmoo(self, message)
			if 'orz' in content.lower():
				await react_orz(self, message)
			if 'pat' in content.lower():
				await react_headpat(self, message)

async def updater(client):
	await client.wait_until_ready()
	await asyncio.sleep(2)
	while not client.is_closed:
		await updateMutes(client)
		await asyncio.sleep(1)

client = MyClient()
client.loop.create_task(updater(client))
client.run(token)

