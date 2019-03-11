import asyncio
from discord import *
from discord.utils import *

async def print_geniosity(bot, message):
    await bot.send_message(message.channel, '<:geniosity:554459617271480321>')

async def react_geniosity(bot, message):
    emoji = get(bot.get_all_emojis(), name='geniosity')
    await bot.add_reaction(message, emoji)