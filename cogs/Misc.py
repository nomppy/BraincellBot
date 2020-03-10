import discord
from discord.ext import commands

from commands.alive import alive


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def alive(self, ctx):
        await alive(ctx)


def setup(bot):
    bot.add_cog(MiscCog(bot))
