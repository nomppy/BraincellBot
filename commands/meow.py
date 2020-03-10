from Core import get_cat_link
from discor.ext import commands


@commands.command(aliases=['catpls', 'plscat', 'bestanimal', 'cat'])
async def meow(ctx):
    async with ctx.typing():
        link = await get_cat_link()
        await ctx.send(embed=discord.Embed().set_image(url=link))
