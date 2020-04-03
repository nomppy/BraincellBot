import discord
from discord.ext import commands
from mods import info, vars_


@commands.command()
async def invite(ctx):
    await ctx.send(embed=discord.Embed(
        title='Click here!',
        colour=ctx.guild.me.colour,
        url='https://discordapp.com/api/oauth2/authorize?client_id=681128428195282947&permissions=117824&scope=bot'
    ))


def setup(bot):
    info.Info(
        name='invite',
        brief='invite me to your server',
        usage='`invite`',
    ).export(vars_.info_)
    bot.add_command(invite)
