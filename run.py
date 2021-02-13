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
token = "" # remove when upload

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

    async def on_message_delete(self, message):
    
        if int(message.channel.id) == int(potdStatusChannelID):
            await fixLeaderboard(self, message)

        if len(message.content) >= 1700:
            private_bot = self.get_channel(655312161064615936)
            await private_bot.send('deleted by ' + str(message.author))
            await private_bot.send(message.content)
            await private_bot.send('-----------')

    async def on_message_edit(self, before, after):
        if len(before.content) >= 1700:
            private_bot = self.get_channel(655312161064615936)
            await private_bot.send('edited by ' + str(before.author))
            await private_bot.send('old message:')
            await private_bot.send(before.content)
            await private_bot.send('-----------')

    async def on_message(self, message):
    
        if("muted" in [y.name.lower() for y in message.author.roles]):
            return

        if (message.author.id == "367469002374774786"):  # imax id
            await react_headpat(self, message)
        if (message.author.id == '384304778173480960'): # karen id
            await react_ayaya(self, message)

        content = message.content

        powerful = ("mooderator" in [y.name.lower() for y in message.author.roles]
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

        if int(message.channel.id) == int(potdStatusChannelID):
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
            elif content.startswith("cp "):
                tipe = content[3:].strip()
                role = discord.utils.get(self.get_guild(ServerID).roles, name = "cp only")
                if tipe == "on":
                    await message.author.add_roles(role)
                    await message.channel.send("cp only has been given")
                elif tipe == "off":
                    await message.author.remove_roles(role)
                    await message.channel.send("cp only has been taken")
                else:
                    await message.channel.send("invalid choice (on/off)")
            elif content.lower().startswith("give "):
                try:
                    roleName = content[27:].strip()
                    if(roleName == "Muted" or roleName == "moot maestro"):
                        raise TypeError("You cannot give a Mute this way.")
                    role = discord.utils.get(self.get_guild(ServerID).roles,name=roleName)
                    if(powerful):                        
                        await message.mentions[0].add_roles(role)
                        await message.channel.send(roleName + " has been given.")
                    else:
                        await message.channel.send("Missing permissions!")
                except:
                    await message.channel.send("The role is nonexistant or too powerful.")
            elif content.lower().startswith("take "):
                try:
                    roleName = content[27:].strip()
                    if(roleName == "Muted" or roleName == "moot maestro"):
                        raise TypeError("You cannot take a Mute this way.")
                    role = discord.utils.get(self.get_guild(ServerID).roles,name=roleName)
                    if(powerful):
                        await message.mentions[0].remove_roles(role)
                        await message.channel.send(roleName + " has been taken.")
                    else:
                        await message.channel.send("Missing permissions!")
                except:
                    await message.channel.send("The role is nonexistant or too powerful.")
            elif content.lower().startswith("internalunmute ") and "orz bot" in [y.name.lower() for y in message.author.roles]:
                await internalUnmute(self, message)
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
                if ('orz' in content.lower()) and not ('antiorz' in content.lower()):
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
        banlist = ['𝓑𝓲𝓼𝔀𝓪𝓭𝓮𝓿 𝓓𝓮𝓿 𝓡𝓸𝔂', '𝗕𝗶𝘀𝘄𝗮𝗱𝗲𝘃 𝗗𝗲𝘃 𝗥𝗼𝘆']
        if any(banned in member.name for banned in banlist):
            await member.ban()
        await self.get_channel(516126151023001610).send("Welcowme <@" + str(member.id) + ">! Please check <#519840263326138378>!")
        await self.get_channel(516126151023001610).send(":pray: :cow:")
        await checkMutes(self, member)

    async def on_member_update(self, before, after):
        oldRoles = [int(y.id) for y in before.roles]
        newRoles = [int(y.id) for y in after.roles]
        if((MutedRoleName in oldRoles and not MutedRoleName in newRoles) or (not MutedRoleName in oldRoles and MutedRoleName in newRoles)):
            await checkMutes(self, after)
            
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == STAR and int(reaction.count) == LIMIT:
            await post_star(self, reaction.message)
        elif str(reaction.emoji) == GENIOSITY and int(reaction.count) == LIMIT and int(reaction.message.channel.id) != int(potdStatusChannelID):
            await post_geniosity(self, reaction.message)
        
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

intents = discord.Intents(guilds=True, members=True, messages=True, reactions=True)
client = MyClient(intents=intents)
client.loop.create_task(updater(client))
client.run(token)

