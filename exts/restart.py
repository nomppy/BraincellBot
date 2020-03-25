import os

from discord.ext import commands


@commands.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send('Restarting...')
    os.system('./restart_bot.bash & disown')


def setup(bot):
    bot.add_command(restart)
