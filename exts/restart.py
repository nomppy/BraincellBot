import os

from discord.ext import commands


@commands.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send('Restarting...')
    os.system('nohup python BraincellBot.py')
    quit()
    # os.system('nohup ./restart_bot.bash &')


def setup(bot):
    bot.add_command(restart)
