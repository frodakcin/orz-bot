import datetime
import time as rateLimitCounter

import requests
import discord
import censor
from eight_ball import *
from geniosity import *
from mute import *
from potd import *
from starboard import *
import sys

prefix = '!'
potdStatusChannelID = '518297095099121665'
token =  # remove when upload

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await updatePOTD()
        print("Finished setting up POTD Leaderboard...")
        await self.change_presence(activity=discord.Game(name="Tmw orz", url="https://codeforces.com/profile/tmwilliamlin168", type=0),
                                   status=Status.online, afk=False)

    async def on_message(self, message):

        if (message.author.id == "367469002374774786"):  # imax id
            await react_headpat(self, message)
        if (message.author.id == '384304778173480960'): # karen id
            await react_ayaya(self, message)

        content = message.content

        powerful = ("moderator" in [y.name.lower() for y in message.author.roles]
                or "admin" in [y.name.lower() for y in message.author.roles]
                or "moot maestro" in [y.name.lower() for y in message.author.roles]
                or "orz bot" in [y.name.lower() for y in message.author.roles])

        if "twice sucks" in message.content.lower() and not (powerful):
            await message.channel.send("!give <@" + message.author.id + "> Muted")
            return
        if "how" in message.content.lower() and ("get better" in message.content.lower() or "improve" in message.content.lower()):
            await message.channel.send("Solve more problems and listen to Twice!")
        if "no u" in message.content.lower() and not "orz bot" in [y.name.lower() for y in message.author.roles]:
            await message.channel.send("no u")

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
                e.add_field(name="POTD", value="\"!points @<User>\" for user's points.\n"+
                                               "\"!leaderboard\" for top 10 users with their points.", inline=False)
                e.add_field(name="Mute", value="\"!mute @<User> <Integer>s\" to mute user for given seconds.\n"+
                                               "\"!mute @<User> <Integer>m\" to mute user for given minutes.\n"+
                                               "\"!mute @<User> <Integer>h\" to mute user for given hours.\n"+
                                               "\"!unmute @<User>\" to unmute user.\n" +
                                               "\"!mutelist\" to get a list of muted users with their end of mute times in UTC.\n", inline=False)
                e.add_field(name="Misc", value="\"!echo <Message>\" to repeat a given message.\n"+
                                               "\"!8ball <Message>\" to get an 8-ball response for a message.\n" +
                                               "\"!give @<User> <Rolename>\" to add specified role to user.\n"+
                                               "\"!take @<User> <Rolename>\" to remove specified role from user.", inline=False)
                await message.channel.send(embed=e)
            elif content.lower().startswith('mute '):
                if(powerful or message.author.id == message.mentions[0].id):
                    await mute(self, message)
                else:
                    await message.channel.send("Missing permissions!")
            elif content.lower().startswith('unmute '):
                if(powerful):
                    await unmute(self, message)
                else:
                    await message.channel.send("Missing permissions!")
            elif content.lower().startswith("mutelist"):
                await getMuteList(self, message)
            elif content.startswith('echo ') and not "!" in content and not "@" in content:
                await message.channel.send(content[5:])
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
                try:
                    roleName = content[27:].strip()
                    role = discord.utils.get(self.get_guild(ServerID).roles,name=roleName)
                    if(powerful):
                        await self.get_guild(ServerID).get_member(message.mentions[0].id).add_roles(role)
                        await message.channel.send(roleName + " has been given.")
                    else:
                        await message.channel.send("Missing permissions!")
                except:
                    await message.channel.send("The role is nonexistant or too powerful.")
            elif content.lower().startswith("take "):
                try:
                    roleName = content[27:].strip()
                    role = discord.utils.get(self.get_guild(ServerID).roles,name=roleName)
                    if(powerful):
                        await self.get_guild(ServerID).get_member(message.mentions[0].id).remove_roles(role)
                        await message.channel.send(roleName + " has been taken.")
                    else:
                        await message.channel.send("Missing permissions!")
                except:
                    await message.channel.send("The role is nonexistant or too powerful.")
        else:
            try:
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
                if 'egg' in content.lower():
                    await react_egg(self, message)
                if 'blobpat' in content.lower():
                    await react_headpat(self, message)
                if 'eggmel' in content.lower() or 'eygmel' in content.lower() or 'stephy15' in content.lower() or 'sarren' in content.lower() or 'aermel' in content.lower() or 'starren' in content.lower() or 'kagebashy15' in content.lower() or 'eygirlwhoisunderage' in content.lower():
                    await react_ship(self, message)
            except:
                pass

    async def on_member_join(self, member):
        await self.get_guild(516125324711297024).get_channel(516126151023001610).send("Welcowme <@" + str(member.id) + ">! Please check <#519840263326138378>!")
        await self.get_guild(516125324711297024).get_channel(516126151023001610).send(":pray: :cow:")
        await checkMutes(self, member)

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == STAR and reaction.count == STAR_LIMIT:
            await post_embed(self, reaction.message)

async def updatePOTD():
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
                headers={"Authorization": "Bot " + token}).text)
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
        rateLimitCounter.sleep(1) # rate-limiting

async def updater(client):
    await client.wait_until_ready();
    while True:
        await asyncio.sleep(1)
        await updateMutes(client)


client = MyClient()
client.loop.create_task(updater(client))
client.run(token)
