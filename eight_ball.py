from discord import *
import asyncio
import random

async def make_prediction(bot, message):
	content = message.content
	parsed = content.lower()
	e = Embed(title=message.author.name + ' asked:', description=content[7:], 
		color=0x9999ff)

	reponse = ''

	# rigged
	if 'eyg' in parsed and 'pedo' in parsed:
		response = 'Eyg is pedo.'
	elif 'fishy' in parsed and 'geniosity' in parsed:
		response = 'Fishy is geniosity.'
	# not rigged
	else:
		response = get_random_message()

	e.add_field(name='Answer:', value=response)
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

