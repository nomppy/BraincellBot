import discord

from mods.core import get_cat_link
from discord.ext import commands
from mods import firestore, info, vars_

aliases = ['catpls', 'plscat', 'bestanimal', 'cat']


@commands.command(aliases=aliases)
@commands.cooldown(1, 4, commands.BucketType.member)
async def meow(ctx):
    if ctx.author.bot:
        return

    async with ctx.typing():
        link = await get_cat_link()
        await ctx.send(embed=discord.Embed().set_image(url=link))
    await firestore.update_command_field(str(ctx.author.id), 'meow', '_last', link)


@meow.error
async def meow_err(ctx, err):
    emb = discord.Embed(
        title='Meow',
        colour=vars_.colour_error
    )
    if isinstance(err, commands.CommandOnCooldown):
        emb.description = f'On cooldown for another {err.retry_after} seconds'
    else:
        emb.description = 'An unknown error has occurred'
    await ctx.send(embed=emb)


def setup(bot):
    info.Info(
        name='meow',
        brief='sends a random cat pic',
        usage='`meow`',
        category='Fun',
        aliases=aliases
    ).export(vars_.info_)

    bot.add_command(meow)
