import datetime
import time as rateLimitCounter
from datetime import *

import requests
import discord
import censor
from eight_ball import *
from geniosity import *
from mute import *
from potd import *

prefix = '!'
potdStatusChannelID = '518297095099121665'
token =  # remove when upload


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        raw = open(PotdDataFilePath, "w")
        raw.write("[\n]")
        raw.close()
        first = ""
        second = "-"
        beforeTag = ""
        while (second != first):
            first = second
            messages = json.loads(
                requests.get(
                    "https://discordapp.com/api/v6/channels/" + potdStatusChannelID + "/messages?limit=100" + beforeTag,
                    headers={"authorization": token}).text)
            for i in messages:
                try:
                    message = i['content']
                    second = i['id']
                    name = i['mentions'][0]['id']
                    nameToShow = i['mentions'][0]['username']
                    if ('pts' in message):
                        content = message[:message.index('pts')].strip()
                        score = min(int(content.split()[-1]), maxPoints)
                    elif ('AC' in message):
                        score = 100
                    elif ('WA' in message or 'TLE' in message or 'MLE' in message or 'CE' in message):
                        score = 0
                    else:
                        content = message.strip()
                        score = min(int(content.split()[-1]), maxPoints)
                    if (score < 0):
                        score = 0
                    updateContender(Contender(name, nameToShow, score))
                    beforeTag = "&before=" + second
                except:
                    pass
            rateLimitCounter.sleep(1)  # rate-limiting
        print("Finished setting up POTD Leaderboard...")

        await self.change_presence(
            game=discord.Game(name="Tmw orz", url="https://codeforces.com/profile/tmwilliamlin168", type=0),
            status=Status.online, afk=False)

    async def on_message(self, message):
        if (message.author.id == "367469002374774786"):  # imax id
            await react_headpat(self, message)

        content = message.content
        if "twice sucks" in message.content.lower() and not (
                "moderator" in [y.name.lower() for y in message.author.roles]
                or "admin" in [y.name.lower() for y in message.author.roles]
                or "moot maestro" in [y.name.lower() for y in message.author.roles]
                or "orz bot" in [y.name.lower() for y in message.author.roles]):
            await self.send_message(message.channel, "!mute <@" + message.author.id + "> 2015h")
            return
        if "how" in message.content.lower() and ("get better" in message.content.lower() or "improve" in message.content.lower()):
            await self.send_message(message.channel, "Solve more problems and listen to Twice!")
	
        if censor.enabled:
            if await censor.isCensored(content.lower()):
                print("Message \"" + content + "\" from user " + message.author.name + " has been deleted.")
                await self.delete_message(message)
                return
        if message.channel.id == potdStatusChannelID:
            await react_geniosity(self, message)
            await updateLeaderboard(self, message)

        if content.startswith(prefix):
            bot_command = True
            content = content[len(prefix):]
            if content.lower().startswith('help'):
                e = Embed(title="Commands")
                e.add_field(name="POTD", value="\"points @<User>\" for user's points.\n"+
                                               "\"leaderboard\" for top 10 users with their points.", inline=False)
                e.add_field(name="Mute", value="\"mute @<User> <Integer>s\" to mute user for given seconds.\n"+
                                               "\"mute @<User> <Integer>m\" to mute user for given minutes.\n"+
                                               "\"mute @<User> <Integer>h\" to mute user for given hours.\n"+
                                               "\"mutelist\" to get a list of muted users with their end of mute times in GMT.\n", inline=False)
                e.add_field(name="Misc", value="\"echo <Message>\" to repeat a given text message.\n"+
                                               "\"8ball <Message>\" to get an 8-ball response for a message.\n" +
                                               "\"give @<User> <Rolename>\" to give user specified role.", inline=False)
                await self.send_message(message.channel, embed=e)
            elif content.lower().startswith('mute ') and ("moderator" in [y.name.lower() for y in message.author.roles]
                                                        or "admin" in [y.name.lower() for y in message.author.roles]
                                                        or "moot maestro" in [y.name.lower() for y in
                                                                              message.author.roles]
                                                        or "orz bot" in [y.name.lower() for y in message.author.roles]
                                                        or message.author.id == message.mentions[0].id):
                await mute(self, message)
            elif content.lower().startswith("mutelist"):
                await getMuteList(self, message)
            elif content.startswith('echo ') and not "!" in content:
                await self.send_message(message.channel, content[5:])
            elif content.startswith('8ball'):
                await make_prediction(self, message)
            elif content.lower().startswith('geniosity'):
                await print_geniosity(self, message)
            elif content.lower().startswith('leaderboard'):
                await getContenderList(self, message)
            elif content.lower().startswith('points'):
                await getContenderData(self, message)
            elif content.startswith("censor "):
                if censor.enabled:
                    await censor.censor_command(self, message.channel, content[7:])
            elif content.lower().startswith("give "):
                role = content[27:].strip()
                if(role == "pusheen fan"):
                    await self.add_roles(message.mentions[0], get_role(self.get_server(ServerID).roles, "pusheen fan"))
                if(role == "vmaddur worshipper"):
                    await self.add_roles(message.mentions[0], get_role(self.get_server(ServerID).roles, "vmaddur worshipper"))

        else:
            if 'tmw' in content.lower():
                await react_tmw(self, message)
            if 'osity' in content.lower():
                await react_geniosity(self, message)
            if 'juicy' in content.lower():
                await react_juicy(self, message)
            if 'wtmoo' in content.lower():
                await react_wtmoo(self, message)
            if 'orz' in content.lower():
                await react_orz(self, message)
            if 'blobpat' in content.lower():
                await react_headpat(self, message)
            if 'egg' in content.lower():
                await react_egg(self, message)
            if 'eggmel' in content.lower() or 'eygmel' in content.lower():
                await react_ship(self, message)


async def updater(client):
    await client.wait_until_ready();
    while not client.is_closed:
        await asyncio.sleep(2)
        await updateMutes(client)


client = MyClient()
client.loop.create_task(updater(client))
client.run(token)
