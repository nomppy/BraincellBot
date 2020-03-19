import discord

from mods.core import get_cat_link
from discord.ext import commands
from mods import firestore, info


@commands.command(aliases=['catpls', 'plscat', 'bestanimal', 'cat'])
async def meow(ctx):
    if ctx.author.bot:
        return

    async with ctx.typing():
        link = await get_cat_link()
        await ctx.send(embed=discord.Embed().set_image(url=link))
        await firestore.update_command(str(ctx.author.id), 'meow', '_last', link)


def setup(bot):
    info.Help(
        name='meow',
        description='sends a picture of a cat',
        usage='`meow`'
    ).export()
    bot.add_command(meow)
