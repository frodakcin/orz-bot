from discord import *
import asyncio 

LIMIT = 6
GALLERY = 577381775739846676
STAR = '⭐'
GENIOSITY = '<:geniosity:516424110205566987>'
MSGS = set()

async def post_star(bot, message):
    if message.id not in MSGS:
        embed = make_star(message)
        await bot.get_channel(GALLERY).send(embed=embed)
        MSGS.add(message.id)

async def post_geniosity(bot, message):
    pass
    '''
    if message.id not in MSGS:
        embed = make_geniosity(message)
        await bot.get_channel(GALLERY).send(embed=embed)
        MSGS.add(message.id)
    '''


def make_star(message):
    
        if(len(message.content) > 256):
            embed = Embed(title =  message.content[:250] + " . . .", description = "[Jump to message](" + message.jump_url + ")", color = 0xffac33)
        else:
            embed = Embed(title =  message.content, description = "[Jump to message](" + message.jump_url + ")", color = 0xffac33)

        embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)

        if message.attachments:
            file = message.attachments[0]
            if str(file.url).lower().endswith(("jpg", "jpeg", "png")):
                embed.set_image(url = file.url)

        return embed


def make_geniosity(message):

        if(len(message.content) > 256):
            embed = Embed(title =  message.content[:250] + " . . .", description = "[Jump to message](" + message.jump_url + ")", color = 0x2ecc71)
        else:
            embed = Embed(title =  message.content, description = "[Jump to message](" + message.jump_url + ")", color = 0x2ecc71)

        embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)

        if message.attachments:
            file = message.attachments[0]
            if str(file.url).lower().endswith(("jpg", "jpeg", "png")):
                embed.set_image(url = file.url)

        return embed
