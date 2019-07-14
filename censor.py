import discord
from discord import *
import asyncio
import json
import abc
from abc import abstractmethod
import string
from string import *

cannotEncodeText = "{0} cannot encode {1}"
cannotDecodeText = "{0} cannot decode {1}"

enabled = False
def assertType(x, t):
	if not isinstance(t, type):
		raise TypeError(t.__class__.__name__ + " is not a type")
	if not isinstance(x, t):
		raise TypeError(x.__class__.__name__ + " is not an instance of " + t.__name__)

class CensorRule:
	
	@abstractmethod
	# Returns boolean as to whether a message is to be censored
	def isCensored(text):
		pass

def CensorRuleEncoder(x):
	if not isinstance(x, CensorRule):
		raise TypeError(cannotEncodeText.format("CensorRule", x.__class__.__name__))
	if x.__class__ == SubstrIncludeWithout:
		return SubstrIncludeWithoutEncoder(x)
	else:
		raise TypeError("CensorRuleEncoder cannot seem to encode")

def CensorRuleDecoder(x):
	if x["type"] == "SubstrIncludeWithout":
		return SubstrIncludeWithoutDecoder(x)
	else:
		raise TypeError("CensorRuleDecoder cannot seem to decode")

class SubstrIncludeWithout(CensorRule):
	def __init__(self, include, without):
		assertType(include, list)
		for x in include:
			assertType(x, str)
		assertType(without, list)
		for x in without:
			assertType(x, str)
		self.include = include
		self.without = without
	def isCensored(self, text):
		for x in self.include:
			if x not in text:
				return False
		for x in self.without:
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

def SubstrIncludeWithoutDecoder(x):
	if x["type"] != "SubstrIncludeWithout":
		raise TypeError(cannotDecodeText.format("SubstrIncludeWithoutDecoder", x["type"]))
	return SubstrIncludeWithout(x["include"], x["without"])


censorRules = []


async def isCensored(content):
	for x in censorRules:
		if x.isCensored(content):
			return True
	return False

censorFile = "censor.json"

async def addRule(client, channel, x):
	I = True
	i = []
	w = []
	for y in x:
		if y[0] == '-':
			if y[1:] == 'i':
				I = True
			elif y[1:] == 'w':
				I = False
			else:
				await client.send_message(channel, "Syntax Error!")
				return
		else:
			if I:
				i.append(y)
			else:
				w.append(y)
	censorRules.append(SubstrIncludeWithout(i, w))
	saveCensor()

async def delRule(client, channel, x):
	if len(x) != 1:
		await client.send_message(channel, "Syntax Error!")
	try:
		x = int(x[0])
	except:
		await client.send_message(channel, "Syntax Error!")
		return
	if x < 0 or x >= len(censorRules):
		await client.send_message(channel, "Index out of bounds!")
		return
	censorRules.pop(x)
	saveCensor()

async def censor_command(client, channel, m):
	x = m.split()
	if x[0] == '+' or x[0] == "add":
		return await addRule(client, channel, x[1:])
	if x[0] == '-' or x[0] == "del":
		return await delRule(client, channel, x[1:])

def saveCensor():
	with open(censorFile, "w") as writeFile:
		json.dump(censorRules, writeFile, default=CensorRuleEncoder, sort_keys=False, indent=2);
def loadCensor():
	global censorRules
	with open(censorFile, "r") as readFile:
		censorRules = json.load(readFile, object_hook=CensorRuleDecoder)

loadCensor()
