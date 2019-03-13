import discord
from discord import *
import asyncio
import json

censoredSets = []

def valid(m):
	for x in censoredSets:
		w = True
		for y in x:
			if y not in m:
				w = False
				break
		if w:
			return False
	return True


async def process(m):
	if not valid(m.message):
		await delete_message(m)
	return False

censorFile = "censor.json"

async def censor_command(m):
	if(m.startsWith('+')):
		# add
	elif(m.starsWith('-')):
		# remove

def save():
	with open(censorFile, "w") as writeFile:
		json.dump(censoredSets, writeFile, indent=2);
def load():
	global censoredSets
	with open(censorFile, "r") as readFile:
		censoredSets = json.load(readFile)
