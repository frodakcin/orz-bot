import asyncio
from discord import *

async def print_geniosity(bot, message):
    await bot.send_message(message.channel, '<:geniosity:554459617271480321>')
