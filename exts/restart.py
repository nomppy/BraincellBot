import os
import sys

from discord.ext import commands


@commands.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send('Restarting...')
    os.execl(sys.executable, sys.executable, * sys.argv)
    # os.system('nohup ./restart_bot.bash &')


def setup(bot):
    bot.add_command(restart)
