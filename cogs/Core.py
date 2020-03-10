import discord
from discord.ext import commands
from commands.newavatar import new_avatar
from commands.meow import meow


class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newpfp(self, ctx, arg='random'):
        async with ctx.typing():
            result = await new_avatar(ctx, arg)
            await ctx.send(result)

    @newpfp.error
    async def newpfp_error(self, ctx, err):
        await ctx.send(err)

    @commands.command(aliases=['catpls', 'plscat', 'bestanimal', 'cat'])
    async def meow(self, ctx):
        async with ctx.typing():
            link = await meow(ctx)
            await ctx.send(embed=discord.Embed().set_image(url=link))


def setup(bot):
    bot.add_cog(CoreCog(bot))
