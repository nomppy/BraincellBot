import random
from discord.ext import commands


class Alive(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_
        self.resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(',
                     'We\'re all gonna die anyway',
                     'What\'s the point?']

    @commands.command()
    async def alive(self, ctx):
        await ctx.send(self.resp[random.randint(0, len(self.resp) - 1)])


def setup(bot):
    bot.add_cog(Alive(bot))
