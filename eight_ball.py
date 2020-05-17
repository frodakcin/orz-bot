import random

from discord import *


async def make_prediction(bot, message):
	content = message.content
	parsed = content.lower()
	e = Embed(title=message.author.name + ' asked:', description=content[7:],
			  color=0x9999ff)

	reponse = ''

	# rigged
	if 'eyg' in parsed or 'pedo' in parsed:
		response = 'Eyg is not pedo.'
	elif 'fishy' in parsed and 'geniosity' in parsed:
		response = 'Fishy is geniosity.'
	elif 'steph' in parsed and 'smart' in parsed:
		response = 'Yes, Steph is super geniosity.'
	elif 'tmw' in parsed or 'who is orz' in parsed:
		response = 'TMW OFZ'
	# not rigged
	else:
		response = get_random_message()

	e.add_field(name='Answer:', value=response)
	await message.channel.send(embed=e)


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
