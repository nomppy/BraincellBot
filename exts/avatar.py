import re

import discord
from discord.ext import commands


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, user=None):
        if re.match(r"^<@!?[0-9]+>$", user):
            user = ctx.message.mentions[0]
            uid = user.id
        elif re.match(r"^[0-9]+$", user):
            uid = int(user)
        else:
            return 'Invalid user.'
        avatar_url = (await self.bot.fetch_user(uid)).avatar_url
        await ctx.send(discord.Embed().set_image(url=avatar_url))
        return avatar_url
