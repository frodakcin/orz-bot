from discord import *
import asyncio
import random

async def make_prediction(bot, message):
	content = message.content
	e = Embed(title=message.author.name, description=content[7:], 
		color=0x9999ff)

	reponse = ''
	response = get_random_message()

	e.add_field(name='answer', value=response)
	await bot.send_message(message.channel, embed=e)

def get_random_message():
	results = [
		'It is certain.',
		'It is decidedly so.',
		'Without a doubt.',
		'Yes - definitely.',
		'You may rely on it.',
		'As I see it, yes.',
		'Most likely.',
		'Outlook good.',
		'Yes.',
		'Signs point to yes.',
		'Reply hazy, try again.',
		'Ask again later.',
		'Better not tell you now.',
		'Cannot predict now.',
		'Concentrate and ask again.',
		'Don\'t count on it.',
		'My reply is no.',
		'My sources say no.',
		'Outlook not so good.',
		'Very doubtful.'
	]

	return random.choice(results)

