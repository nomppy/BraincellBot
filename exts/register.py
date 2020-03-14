from discord.ext import commands
from mods import token
from mods import firestore


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        if ctx.author.bot:
            return -1

        user = ctx.author

        def dm_reply(m):
            return m.channel == user.dm_channel

        await user.send('Hello! Please reply with either the required information or with `self` to self-host')
        await user.send('Please start with your token:')
        resp = await self.bot.check_for('message', timeout=30.0, check=dm_reply)
        if resp == 'self':
            await user.send('Alright, head here and follow the instructions to get started: '
                            'https://repl.it/@kenhtsun/BraincellBot-Client')
            custom_token = await token.create_custom_token(ctx.author)
            await user.send(f'Your unique token is ||{custom_token}||. Keep this token safe!')
