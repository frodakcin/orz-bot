import discord
from discord import *
import asyncio
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
			content = content[len(prefix):]
			if content.startswith("echo "):
				await self.send_message(message.channel, content[5:])
			elif content.lower().startswith('geniosity'):
				await print_geniosity(self, message)
		elif 'geniosity' in content.lower():
			await react_geniosity(self, message)
		elif 'wtmoo' in content.lower():
			await react_wtmoo(self, message)

client = MyClient()
client.run(input())

