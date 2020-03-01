from discord import *
import asyncio 

STAR_LIMIT = 3
STARBOARD = 577381775739846676
STAR = '⭐'
STARRED_MSGS = set()

async def post_embed(bot, message):
    if message.id not in STARRED_MSGS:
        embed = make_embed(message)
        await bot.get_channel(STARBOARD).send(embed=embed)
        STARRED_MSGS.add(message.id)


def make_embed(message):
        embed = Embed()

        if message.content:
            embed.add_field(name = 'message', value = message.content, inline = False)

        if message.attachments:
            file = message.attachments[0]
            if str(file.url).endswith(('jpg', 'jpeg', 'png')):
                embed.set_image(url = file.url)

        embed.add_field(name = 'link', value = '[click me](' + message.jump_url + ')')
        embed.set_footer(text = str(message.author), icon_url = message.author.avatar_url)
        return embed