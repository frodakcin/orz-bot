import datetime
from datetime import *
import pytz
import json
import time
import discord
from discord import *

MuteDataFilePath = "mute.json"
ServerID = 516125324711297024
MutedRoleName = 563584831510937600
muteList = []


def get_role(server_roles, target_name):
    for each in server_roles:
        if each.name == target_name:
            return each
    return None


class Muted:
    def __init__(self, user, name, when):
        self.user = user
        self.name = name
        self.endOfMute = when

    def __lt__(self, other):
        if (self.endOfMute.replace(tzinfo=pytz.utc) != other.endOfMute.replace(tzinfo=pytz.utc)):
            return self.endOfMute.replace(tzinfo=pytz.utc) < other.endOfMute.replace(tzinfo=pytz.utc)
        return self.user < other.user 

    def __gt__(self, other):
        if (self.endOfMute.replace(tzinfo=pytz.utc) != other.endOfMute.replace(tzinfo=pytz.utc)):
            return self.endOfMute.replace(tzinfo=pytz.utc) > other.endOfMute.replace(tzinfo=pytz.utc)
        return self.user > other.user

    def increase_mute_length(self, penalty):
        self.endOfMute += penalty;

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toString(self):
        return self.endOfMute.strftime("%B %d, %Y at %H:%M:%S")


def insertMuted(x):
    if isinstance(x, Muted):
        A = True
        for i in range(len(muteList)):
            if (x < muteList[i]):
                muteList.insert(i, x)
                A = False
                break
        if (A):
            muteList.append(x)
        save()
    else:
        raise TypeError("You can only insert Muted objects!")


async def mute(bot, message):
    if (("moderator" in [y.name.lower() for y in message.mentions[0].roles]
         or "admin" in [y.name.lower() for y in message.mentions[0].roles]
         or "moot maestro" in [y.name.lower() for y in message.mentions[0].roles]
         or "orz bot" in [y.name.lower() for y in message.mentions[0].roles])
            and message.mentions[0].id != message.author.id):
        await message.channel.send("Target user has the ability to remove the mute!")
        return
    try:
        content = (message.content[5:]).split()
        name = message.mentions[0].id
        username = message.mentions[0].name
        amount = int(content[1][:-1])
        timeUnit = content[1][-1:]
        role = discord.utils.get(bot.get_guild(ServerID).roles,id=MutedRoleName)
        if ((name == message.author.id and amount < 0) and not ("moderator" in [y.name.lower() for y in message.mentions[0].roles]
             or "admin" in [y.name.lower() for y in message.mentions[0].roles]
             or "moot maestro" in [y.name.lower() for y in message.mentions[0].roles])):
            await message.channel.send('Nice try.')
            await message.channel.send(
                                   "!mute <@" + message.author.id + "> " + str(-1 * int(amount)) + timeUnit)
            return

        if (timeUnit == 's'):
            for i in range(len(muteList)):
                if (muteList[i].user == name):
                    insertMuted(Muted(name, username, muteList.pop(i).endOfMute + timedelta(seconds=amount)))
                    await message.channel.send(
                                           username + ' has been muted for ' + str(amount) + ' more second(s).')
                    return
            insertMuted(Muted(name, username, datetime.now(pytz.utc) + timedelta(seconds=amount)))
            await message.channel.send(username + ' has been muted for ' + str(amount) + ' second(s).')
            await bot.get_guild(ServerID).get_member(name).add_roles(role)

        elif (timeUnit == 'm'):
            for i in range(len(muteList)):
                if (muteList[i].user == name):
                    insertMuted(Muted(name, username, muteList.pop(i).endOfMute + timedelta(minutes=amount)))
                    await message.channel.send(
                                           username + ' has been muted for ' + str(amount) + ' more minute(s).')
                    return
            insertMuted(Muted(name, username, datetime.now(pytz.utc) + timedelta(minutes=amount)))
            await message.channel.send(username + ' has been muted for ' + str(amount) + ' minute(s).')
            await bot.get_guild(ServerID).get_member(name).add_roles(role)

        elif (timeUnit == 'h'):
            for i in range(len(muteList)):
                if (muteList[i].user == name):
                    insertMuted(Muted(name, username, muteList.pop(i).endOfMute + timedelta(hours=amount)))
                    await message.channel.send(
                                           username + ' has been muted for ' + str(amount) + ' more hour(s).')
                    return
            insertMuted(Muted(name, username, datetime.now(pytz.utc) + timedelta(hours=amount)))
            await message.channel.send(username + ' has been muted for ' + str(amount) + ' hour(s).')
            await bot.get_guild(ServerID).get_member(name).add_roles(role)

        else:
            raise ValueError(timeUnit + " is not a valid Time Unit.");

    except:
        await message.channel.send("Invalid mute!")

async def unmute(bot, message):
    role = discord.utils.get(bot.get_guild(ServerID).roles,id=MutedRoleName)
    name = message.mentions[0].id
    username = message.mentions[0].name
    found = False
    for i in range(len(muteList)):
        if (muteList[i].user == name):
            muteList[i].endOfMute = datetime.now(pytz.utc)
            found = True
            break
    if(found):
        await message.channel.send(username + " has been unmuted.")
    else:
        await message.channel.send(username + " is not muted.")
        for i in range(len(muteList)):
            print(muteList[i].user)
            print(name)

async def getMuteList(bot, message):
    e = Embed(title="Mute List")
    for i in range(len(muteList)):
        e.add_field(name=muteList[i].name,
                    value=Muted(muteList[i].user, muteList[i].name, muteList[i].endOfMute).toString(), inline=False)
    await message.channel.send(embed=e)

async def checkMutes(bot, member):
    role = discord.utils.get(bot.get_guild(ServerID).roles,id=MutedRoleName)
    for i in muteList:
        if(i.user==member.id):
            await member.add_roles(role)

async def updateMutes(bot):
    varLEN = len(muteList)
    i = 0
    role = discord.utils.get(bot.get_guild(ServerID).roles,id=MutedRoleName)
    while (i < varLEN):
        if (muteList[i].endOfMute.replace(tzinfo=pytz.utc) < datetime.now(pytz.utc)):
            x = muteList.pop(i).user
            time.sleep(2)
            try:
                await bot.get_guild(ServerID).get_member(x).remove_roles(role)
            except:
                pass
            i -= 1
            varLEN -= 1
        i += 1
    save()


# START IO
def encode_datetime(dt):
    if isinstance(dt, datetime):
        return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    else:
        raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_datetime")


def encode_Muted(x):
    if isinstance(x, Muted):
        return {"user": (x.user), "name": (x.name), "when": encode_datetime(x.endOfMute)}
    else:
        raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_Muted")


def get_datetime(x):
    return datetime(x[0], x[1], x[2], x[3], x[4], x[5])


def decode_Muted(x):
    return Muted(x["user"], x["name"], get_datetime(x["when"]))


def save():
    with open(MuteDataFilePath, "w") as write_file:
        json.dump(muteList, write_file, default=encode_Muted, sort_keys=False, indent=2)


def load():
    global muteList
    with open(MuteDataFilePath, "r") as read_file:
        muteList = json.load(read_file, object_hook=decode_Muted)


# END IO

load()
