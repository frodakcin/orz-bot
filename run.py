import discord
from discord import *
import asyncio
from eight_ball import *
from geniosity import *

prefix = '!'

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
		
		if content.startswith(prefix):
			bot_command = True
			content = content[len(prefix):]
			if content.startswith("echo "):
				await self.send_message(message.channel, content[5:])
			elif content.startswith('8ball'):
				await make_prediction(self, message)
			elif content.lower().startswith('geniosity'):
				await print_geniosity(self, message)
		else:
			if 'geniosity' in content.lower():
				await react_geniosity(self, message)
			if 'wtmoo' in content.lower():
				await react_wtmoo(self, message)
			if 'orz' in content.lower():
				await react_orz(self, message)

client = MyClient()
client.run(input())

