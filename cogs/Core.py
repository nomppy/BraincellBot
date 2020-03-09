from discord.ext import commands
from Core import *


class CoreCog(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alias=['catpls', 'plscat', 'bestanimal', 'cat'])
    async def meow(self, ctx):
        async with ctx.typing():
            image_link = await get_cat_link()
            import discord
            await ctx.send(embed=discord.Embed().set_image(url=image_link))  # embeded image

    @commands.command()
    async def newpfp(self, ctx, arg='random'):
        async with ctx.typing():
            if arg[-3:] in ['jpg', 'png']:
                img_link = arg
            elif len(ctx.message.attachments) == 1:
                img_link = ctx.message.attachments[0].url
            elif arg == 'random':
                img_link = await get_cat_link()
            else:
                return 'Are you sure you called the command correctly?'
            # print(img_link)
            return await change_avatar(img_link)

    @newpfp.error
    async def newpfp_error(self, ctx, err):
        print(err)
        await ctx.send(err)


def setup(bot):
    bot.add_cog(CoreCog(bot))
