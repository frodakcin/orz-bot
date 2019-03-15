import discord
from discord import *
import asyncio
from mute import *
from eight_ball import *
from geniosity import *
import censor
from potd import *

prefix = '!'
potdStatusChannelID = '555527539779567657'

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
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
			await updateLeaderboard(self, message)f

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
client.run(input())
