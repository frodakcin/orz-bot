from discord import *
import asyncio

async def make_prediction(bot, message):
    content = message.content
    e = Embed(title=message.author.name, description=content, 
        color=0x9999ff)

    reponse = ''
    response = get_random_message()

    e.add_field(name='answer', value=response)
    await bot.send_message(message.channel, embed=e)

def get_random_message():
    return 'test'