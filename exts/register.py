from discord.ext import commands
from firebase_admin.auth import UserNotFoundError

from mods import token
from mods import firestore


async def _self_host(uid: str):
    custom_token = token.create_custom_token(uid).decode('utf-8')
    firestore.add_user(uid, True, custom_token)
    return 'Alright, head here and follow the instructions to get started:  ' \
           'https://repl.it/@kenhtsun/BraincellBot-Client \n' \
           f'Your unique token is ```{custom_token}```' \
           'Keep this token safe! '


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_user_reply(self, user):
        def dm_reply(m):
            return m.guild is None and m.author == user

        try:
            resp = await self.bot.wait_for('message', timeout=30.0, check=dm_reply)
        except TimeoutError:
            return
        return resp.content

    async def _get_user_token(self, user):
        # TODO check if entered token is plausible
        await user.send(
            'Enter your discord token here, your token is required for the bot to change your status message.\n'
            'So you can enter `none` if you dont want that function.')
        try:
            resp = await self._get_user_reply(user)
        except TimeoutError:
            return
        if resp == 'none':
            return None
        else:
            return resp

    async def _get_user_email(self, user):
        # TODO same thing here, use regex to see if it's a valid email
        await user.send('Enter the email you used to sign up for discord, this is needed to change your avatar\n'
                        'You can also enter `none` if you want to opt-out.')
        try:
            resp = await self._get_user_reply(user)
        except TimeoutError:
            return
        if resp.lower() == 'none':
            return None
        else:
            return resp

    async def _get_user_pwd(self, user):
        await user.send('Finally, enter your discord password, this is also needed to change your avatar\n'
                        'As always, enter `none` if you want')
        try:
            resp = await self._get_user_reply(user)
        except TimeoutError:
            return
        if resp.lower() == 'none':
            return None
        else:
            return resp

    @commands.command()
    async def register(self, ctx):
        if ctx.author.bot:
            return

        user = ctx.author
        uid = str(user.id)

        async def _send_current_info(__user):
            _user = firestore.get_user(str(__user.id))
            _token = _user['token']
            _email = _user['email']
            _pwd = _user['pwd']
            _self = _user['self']
            await __user.send(f'Here\'s what we have on file for you:\n'
                              f'Token: {_token}\n'
                              f'Email: {_email}\n'
                              f'Password: {_pwd}\n'
                              f'Self-hosting: {_self}\n'
                              f'If you want to change any of those just type the corresponding field')

        async def _complete_user_info(__user):
            await _send_current_info(__user)
            resp_ = await self._get_user_reply(user)
            if resp_.lower() == 'self':
                await user.send(await _self_host(uid))
                return
            elif resp_.lower() == 'token':
                new_token = await self._get_user_token(user)
                firestore.update_user(uid, False, new_token=new_token)
            elif resp_.lower() == 'email':
                new_email = await self._get_user_email(user)
                firestore.update_user(uid, False, new_email=new_email)
            elif resp_.lower() in ['pwd', 'password']:
                new_pwd = await self._get_user_pwd(user)
                firestore.update_user(uid, False, new_pwd=new_pwd)
            await _complete_user_info(__user)

        user_ = firestore.get_user(uid)
        if user_:  # user is in database
            token_ = user_['token']
            self_ = user_['self']
            active_ = user_['active']
            if self_:  # registered and self hosting
                await ctx.send('You\'re already registered, dming you your token')
                await user.send(f'Here\'s your token again, don\'t lose it this time! ```{token_}```\n'
                                f'Did you want to revoke or regenerate your token? Use revoke & refresh'
                                f'If you want to switch to letting the bot manage everything for you, revoke '
                                f'your token with revoke and do register again')
                # TODO user react to delete message
            else:
                if active_:  # account is active
                    await ctx.send('You\'re already registered!')
                    await _send_current_info(user)
                else:  # account deactivated
                    await ctx.send('You seem to have deactivated your account, I will need to acquire your credentials '
                                   'again.')
                    await _complete_user_info(user)

        else:
            await user.send('Hello! Please reply with either the required information or with `self` to self-host')
            try:
                resp = await self._get_user_token(user)
            except TimeoutError:
                return
            if resp == 'self':
                await user.send(await _self_host(uid))
            else:
                token_ = resp
                email = await self._get_user_email(user)
                pwd = await self._get_user_pwd(user)
                firestore.add_user(uid, self_=False, token=token_, email=email, pwd=pwd)
                await user.send('That\'s it! The bot can now change your status and avatar. The default prefix is '
                                '`b!`\n '
                                'If at anytime you need to change the information you entered or switch to '
                                'self-hosting, '
                                'just run register again')


def setup(bot):
    bot.add_cog(Register(bot))
