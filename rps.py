from discord import *
import asyncio
import random

choices = ['rock', 'paper', 'scissors']

async def run_game(bot, message, user_choice):
	user_choice = ''
	try:
		user_choice = message.content.split(' ')[1]
	except:
		await bad_user(bot, message)
		return 

	if user_choice == 'r':
		user_choice = 'rock'
	elif user_choice == 'p':
		user_choice = 'paper'
	elif user_choice == 's':
		user_choice = 'scissors'

	if user_choice not in choices:
		await bad_user(bot, message)
		return

	comp_choice = random_response()
	

def random_response():
	return random.choice(choices)

async def bad_user(bot, message):
	await bot.send_message(message.channel, 
		'You must choose \'rock\', \'paper\', or \'scissors\'.')