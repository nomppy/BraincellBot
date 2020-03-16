from discord.ext import commands


class SetPrefix(commands.Cog):
    def __init__(self, bot_):
        self.bot_ = bot_

    @commands.command(aliases=['prefix'])
    async def setprefix(self, ctx, prefix):
        if ctx.author.bot:
            return
        
        if prefix == '':
            await ctx.send('Plz don\'t make the prefix nothing')
            return
        self.bot_.command_prefix = prefix
        await ctx.send(f'Your prefix has been changed to `{prefix}`')


def setup(bot):
    bot.add_cog(SetPrefix(bot))
