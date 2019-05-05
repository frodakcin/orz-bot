import discord
from discord import *
import requests
import asyncio
from mute import *
from eight_ball import *
from geniosity import *
import censor
from potd import *

prefix = '!'
potdStatusChannelID = '518297095099121665'
token = #remove when upload
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		raw = open(PotdDataFilePath, "w")
		raw.write("[\n]")
		raw.close()
		messages = json.loads(requests.get("https://discordapp.com/api/v6/channels/" + potdStatusChannelID + "/messages", headers={"authorization": token}).text)
		for i in messages:
			var = i['content']
			name = i['mentions'][0]['id']
			nameToShow = i['mentions'][0]['username']
			if('pts'in var):
				content=var[:var.index('pts')].strip()
			else:
				content=var.strip()
			score = min(int(content.split()[-1]),maxPoints)
			if(score<0):
				score = 0
			updateContender(Contender(name, nameToShow, score))
		load()
		await self.change_presence(game=discord.Game(name="Tmw orz", url="https://codeforces.com/profile/tmwilliamlin168", type=0), status=Status.online, afk=False)
	
	async def on_message(self, message):
		if message.author == self.user:
			return
		content = message.content
		await updateMutes(self)	
		
		if censor.enabled:
			if await censor.isCensored(content.lower()):
				print("Message \"" + content + "\" from user " + message.author.name + " has been deleted.")
				await self.delete_message(message)
				return
		if message.channel.id == potdStatusChannelID:
			print("message recieved")
			await updateLeaderboard(self, message)
		
		if content.startswith(prefix):
			bot_command = True
			content = content[len(prefix):]
			if content.lower().startswith('mute '):
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
			if 'geniosity' in content:
				await react_geniosity(self, message)
			if 'wtmoo' in content:
				await react_wtmoo(self, message)
			if 'orz' in content:
				await react_orz(self, message)
			if 'juicy' in content:
				await react_juicy(self, message)
			if 'tmw' in content:
				await react_tmw(self, message)

client = MyClient()
client.run(token)
