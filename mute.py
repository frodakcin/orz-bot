import datetime
from datetime import timedelta
import json
import discord
from discord import *

MuteDataFilePath = "mute.json"

muteList = []

class Muted:
    def __init__(self, user, when):
        self.user = user
        self.endOfMute = when

    def __lt__ (self, other):
        if(endOfMute != other.endOfMute):
            return endOfMute < other.endOfMute
        return self.user.id < other.user.id

    def __gt__ (self, other):
        if(endOfMute != other.endOfMute):
            return endOfMute > other.endOfMute
        return self.user.id > other.user.id

    def increase_mute_length(self, penalty):
        self.endOfMute += penalty;

    def toJSON(self):
        return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)

def insertMuted(x):
    if isinstance(x, Muted):
        for i in range(len(muteList)):
            if(x.endOfMute<=muteList[i].endOfMute):
                muteList.insert(i,encode_Muted(x))
                break
        if(len(muteList)==0):
            muteList.append(encode_Muted(x))
        save()
    else:
        raise TypeError("You can only insert Muted objects.")


async def mute(bot, message):
    #try:
    if(1==1):
        content = (message.content).split()
        name = content[1]
        amount = int(content[2][:-1])
        timeUnit = content[2][-1:]
        if(timeUnit=='s'):
            load()
            for i in range(len(muteList)):
                if(decode_Muted(muteList[i]).user == name):
                    insertMuted(Muted(name, Muted(muteList.pop(i)).endOfMute + timedelta(days=amount)))
                    await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more second(s).')
                    return
            insertMuted(Muted(name, datetime.datetime.now() + timedelta(seconds=amount)))
            await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' second(s).')
        elif(timeUnit=='m'):
            load()
            for i in range(len(muteList)):
                if(decode_Muted(muteList[i]).user == name):
                    insertMuted(Muted(name, Muted(muteList.pop(i)).endOfMute + timedelta(minutes=amount)))
                    await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more minute(s).')
                    return
            insertMuted(Muted(name, datetime.datetime.now() + timedelta(minutes=amount)))

            await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' minute(s).')
        elif(timeUnit=='h'):
            load()
            for i in range(len(muteList)):
                if(decode_Muted(muteList[i]).user == name):
                    insertMuted(Muted(name, Muted(muteList.pop(i)).endOfMute + timedelta(hours=amount)))
                    await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more hour(s).')
                    return
            insertMuted(Muted(name, datetime.datetime.now() + timedelta(hours=amount)))

            await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' hour(s).')
        elif(timeUnit=='d'):
            load()
            for i in range(len(muteList)):
                if(decode_Muted(muteList[i]).user == name):
                    insertMuted(Muted(name, Muted(muteList.pop(i)).endOfMute + timedelta(days=amount)))
                    await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' more day(s).')
                    return
            insertMuted(Muted(name, datetime.datetime.now() + timedelta(days=amount)))
            await bot.send_message(message.channel, name+' has been muted for '+str(amount)+' day(s).')
        else:
            raise ValueError
    #except:
        #await bot.send_message(message.channel, 'Invalid format.')

#START IO
MuteDataFilePath = "mute.json"
def encode_datetime(dt):
    if isinstance(dt, datetime.datetime):
        return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    else:
        raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_datetime")
    
def encode_Muted(x):
    if isinstance(x, Muted):
        return {"user": (x.user), "when": encode_datetime(x.endOfMute)}
    else:
        raise TypeError("Object of type {dt.__class__.__name__} is not compatible with encode_Muted")
    
def get_datetime(x):
    return datetime(x[0], x[1], x[2], x[3], x[4], x[5])

def decode_Muted(x):
    return Muted(x["user"], get_datetime(x["when"]))

def save():
    with open(MuteDataFilePath, "w") as write_file:
        json.dump(muteList, write_file, default=encode_Muted, sort_keys=False, indent=2)
        
def load():
    global muteList
    with open(MuteDataFilePath, "r") as read_file:
        muteList = json.load(read_file, object_hook=decode_Muted)
#END IO


"""
load()
print (str(len(muteList)))
for x in muteList:
	print("user: {x.id}, " + str(x.endOfMute))
"""
