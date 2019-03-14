import discord
from discord import *
import asyncio
from mute import *
from eight_ball import *
from geniosity import *
import censor

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
		
		if await censor.isCensored(content.lower()):
			print("Message \"" + content + "\" from user " + message.author.name + " has been deleted.")
			await self.delete_message(message)
			return
		if content.startswith(prefix):
			bot_command = True
			content = content[len(prefix):]
			if content.startswith("censor "):
				await censor_command(content[7:])


client = MyClient()
client.run(input())
