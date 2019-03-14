import discord
from discord import *
import asyncio
import json

cannotEncodeText = "{encodername} cannot encode {classname}"
class censorRule:
	
	@abstractmethod
	# Returns boolean as to whether a message is to be censored
	def isCensored(text):
		pass

class SubstrIncludeWithout(censorRule):
	include = []
	without = []
	def isCensored(text):
		for x in include:
			if x not in text:
				return False
		for x in without:
			if x in text:
				return False
		return True

def SubstrIncludeWithoutEncoder(x):
	if x.__class__ != SubstrIncludeWithout:
		raise TypeError(cannotEncodeText.format("SubstrIncludeWithoutEncoder", x.__class__.__name__))
	r = {"type": "SubstrIncludeWithout", "include": [], "without": []}
	for y in x.include:
		r["include"].append(y)
	for y in x.without:
		r["without"].append(y)
	return r



censorRules = []

def valid(m):
	for x in censorRules:
		w = True
		for y in x:
			if y not in m:
				w = False
				break
		if w:
			return False
	return True


async def isCensored(content):
	return not valid(content)

censorFile = "censor.json"


def addU(x):
	if isinstance(x, list):
		for y in x:
			if not isinstance(x, str):
				raise TypeError("You can only add a list of strings")
		
	else:
		raise TypeError("You can only add a list of strings")

def censor_command(m):
	if(m.startsWith('+')):
		 add

def encode_censorItem(m):
	
def saveCensor():
	with open(censorFile, "w") as writeFile:
		json.dump(censorRules, writeFile, indent=2);
def loadCensor():
	global censorRules
	with open(censorFile, "r") as readFile:
		censorRules = json.load(readFile)

loadCensor()