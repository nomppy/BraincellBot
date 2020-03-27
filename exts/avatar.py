import re
import discord

from discord.ext import commands

from mods import vars_


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, user=None):
        if not user:
            user = str(ctx.message.author.id)
        url = await self.get_avatar(user)
        embed = discord.Embed(
            title='Avatar'
        )
        if not url:
            embed.description = 'Invalid user.'
            embed.colour = vars_.colour_error
            await ctx.send(embed=embed)
            return
        embed.colour = vars_.colour_success
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    async def get_avatar(self, user):
        match = re.search(r"[0-9]+", user)
        if match:
            uid = match.group(0)
        else:
            return
        user = self.bot.get_user(uid)
        if not user:
            return
        avatar_url = user.avatar_url
        return avatar_url


def setup(bot):
    bot.add_cog(Avatar(bot))
