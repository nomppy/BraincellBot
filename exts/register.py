from discord.ext import commands
from mods import token
from mods import firestore


async def _self_host(uid: str):
    custom_token = token.create_custom_token(uid).decode('utf-8')
    firestore.add_user(uid, True, custom_token)
    return 'Alright, head here and follow the instructions to get started:  ' \
           'https://repl.it/@kenhtsun/BraincellBot-Client \n' \
           f'Your unique token is ```{custom_token}```. ' \
           'Keep this token safe! '


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_user_reply(self, user):
        def dm_reply(m):
            return m.guild is None and m.author == user

        resp = await self.bot.wait_for('message', timeout=30.0, check=dm_reply)
        return resp

    async def _get_user_token(self, user):
        # TODO check if entered token is plausible
        user.send('Enter your discord token here, your token is required for the bot to change your status message.\n'
                  'So you can enter `none` if you dont want that function.')
        resp = await self._get_user_reply(user)
        if resp in ['none', 'None']:
            return None
        else:
            return resp

    async def _get_user_email(self, user):
        # TODO same thing here, use regex to see if it's a valid email
        user.send('Enter the email you used to sign up for discord, this is needed to change your avatar\n'
                  'You can also enter `none` if you want to opt-out.')
        resp = await self._get_user_reply(user)
        if resp in ['none', 'None']:
            return None
        else:
            return resp

    async def _get_user_pwd(self, user):
        user.send('Finally, enter your discord password, this is also needed to change your avatar\n'
                  'As always, enter `none` if you want')
        resp = await self._get_user_reply(user)
        if resp in ['none', 'None']:
            return None
        else:
            return resp

    @commands.command()
    @commands.is_owner()
    async def register(self, ctx):
        if ctx.author.bot:
            return -1

        user = ctx.author
        if token.token_exists(user.id):
            self_ = firestore.self_hosting(user.id)
            if self_:
                await ctx.send('You\'re already registered, dming you your token')
                user_token = firestore.get_user_token(user.id)
                await user.send(f'Here\'s your token again, don\'t lose it this time! ```{user_token}```\n'
                                f'Did you want to revoke or regenerate your token? Use revoke & refresh')
                # TODO user react to delete message
            else:
                # TODO func to get uncompleted information, then request for those specifically
                await ctx.send('I already have your token, but I\'send it to you if you want to verify')
                await user.send(f'Here\'s your discord token, according to the information you entered.\n'
                                f'If you wish to change it just enter it right now or enter `self` to switch'
                                f'to self hosting')
                resp = await self._get_user_token(user)
                if resp == 'self':
                    await user.send(_self_host(str(user.id)))
                else:
                    firestore.update_user(str(user.id), False, new_token=resp)
        else:
            def dm_reply(m):
                return m.guild is None and m.author == user

            await user.send('Hello! Please reply with either the required information or with `self` to self-host\n'
                            'Please start with your token:')
            resp = await self.bot.wait_for('message', timeout=30.0, check=dm_reply)
            if resp.content == 'self':
                await user.send(_self_host(str(user.id)))
            else:
                token_ = resp
                email = self._get_user_email(user)
                pwd = self._get_user_pwd(user)
                firestore.add_user(user.id, self_=False, token=token_, email=email, pwd=pwd)
                await user.send('That\'s it! The bot can now change your status and avatar. The default prefix is '
                                '`b!`\n '
                                'If at anytime you need to change the information you entered or switch to '
                                'self-hosting, '
                                'just run register again')


def setup(bot):
    bot.add_cog(Register(bot))
