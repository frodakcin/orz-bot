import discord
from discord import *
import asyncio

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



client = MyClient()
client.run(input())

