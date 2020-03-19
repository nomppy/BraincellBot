import asyncio

from discord.ext import commands

from mods import token, vars_, firestore, info


async def _add_commands_settings(uid: str):
    cmds = vars_.info_
    for cmd in cmds:
        if cmds[cmd].configurable():
            defaults = cmds[cmd].get_defaults()
            for field in defaults:
                if defaults[field] == 'self':
                    defaults[field] = [uid]
            await firestore.update_command_fields(uid, cmd, defaults)


async def _self_host(user):
    uid = str(user.id)
    custom_token = token.create_custom_token(uid).decode('utf-8')
    await firestore.update_user(uid, True, username=user.name, new_token=custom_token, prefix='b!')
    await _add_commands_settings(uid)

    # [await firestore.update_command_fields(uid, cmd, cmds[cmd].get_defaults()) for cmd in cmds]

    # await firestore.update_command_fields(uid, 'counter', {
    #     'template': 'Braincell Counter: $COUNTER$',
    #     'whitelist': uid,
    #     'enabled': True,
    #     'c': 0,
    #     'status': 'Braincell Counter: 0'
    # })
    return 'Alright, head here and follow the instructions to get started:  ' \
           'https://repl.it/@kenhtsun/BraincellBot-Client \n' \
           f'Your unique token is ```{custom_token}```' \
           'Keep this token safe!'


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_user_reply(self, user):
        def dm_reply(m):
            return m.guild is None and m.author == user

        try:
            resp = await self.bot.wait_for('message', timeout=45, check=dm_reply)
        except asyncio.TimeoutError:
            return
        return resp.content

    async def _get_user_token(self, user):
        # TODO check if entered token is plausible
        await user.send(
            'Enter your discord token here, your token is required for the bot to change your status message.\n'
            'So you can enter `none` if you dont want that function.')
        resp = await self._get_user_reply(user)
        if resp == 'none':
            return None
        else:
            return resp

    async def _get_user_email(self, user):
        # TODO same thing here, use regex to see if it's a valid email
        await user.send('Enter the email you used to sign up for discord, this is needed to change your avatar\n'
                        'You can also enter `none` if you want to opt-out.')
        resp = await self._get_user_reply(user)
        if resp.lower() == 'none':
            return None
        else:
            return resp

    async def _get_user_pwd(self, user):
        await user.send('Enter your discord password, this is also needed to change your avatar\n'
                        'As always, enter `none` if you want')
        resp = await self._get_user_reply(user)
        if resp.lower() == 'none':
            return None
        else:
            return resp

    async def _get_user_prefix(self, user):
        await user.send('Now enter your preferred prefix for the bot, this can be changed at any time with the '
                        '`prefix [new_prefix]` command.')
        resp = await self._get_user_reply(user)
        if resp.lower() == 'none':
            await user.send("That\'s an invalid prefix.")
            await self._get_user_prefix(user)
        else:
            return resp

    @commands.command()
    async def register(self, ctx):
        if ctx.author.bot:
            return

        user = ctx.author
        uid = str(user.id)

        async def _send_current_info():
            _user = await firestore.get_user(str(user.id))
            _username = _user['username']
            _token = _user['token']
            _email = _user['email']
            _pwd = _user['pwd']
            _self = _user['self']
            _prefix = _user['prefix']
            _active = _user['active']
            await user.send(f'Here\'s what we have on file for you:```\n'
                            f'Username: {_username}\n'
                            f'Token: {_token}\n'
                            f'Email: {_email}\n'
                            f'Password: {_pwd}\n'
                            f'Prefix: {_prefix}\n'
                            f'Active: {_active} (type active to toggle activation)\n'
                            f'Self-hosting: {_self} '
                            '(type self to switch to self-hosting, all current information will be wiped)```'
                            'If you want to change any of those just type the corresponding field, if not, '
                            'just don\'t type anything (duh). \n'
                            'Also, you only have 45 seconds to reply and then you will DIE')

        async def _complete_user_info():
            if not user_['username']:
                await firestore.update_field(uid, 'username', user.name)
            await _send_current_info()
            resp_ = await self._get_user_reply(user)
            if not resp_:
                return
            resp_ = resp_.lower()
            if resp_ == 'self':
                await user.send(await _self_host(user))
            elif resp_ == 'token':
                new_token = await self._get_user_token(user)
                await firestore.update_field(uid, 'token', new_token)
            elif resp_ == 'email':
                new_email = await self._get_user_email(user)
                await firestore.update_field(uid, 'email', new_email)
            elif resp_ in ['pwd', 'password']:
                new_pwd = await self._get_user_pwd(user)
                await firestore.update_field(uid, 'pwd', new_pwd)
            elif resp_ == 'prefix':
                new_prefix = await self._get_user_prefix(user)
                await firestore.update_field(uid, 'prefix', new_prefix)
            elif resp_ == 'active':
                curr = user_['active']
                await firestore.update_field(uid, 'active', not curr)
            await _complete_user_info()

        user_ = await firestore.get_user(uid)
        if user_:  # user is in database
            token_ = user_['token']
            self_ = user_['self']
            active_ = user_['active']
            if self_:  # registered and self hosting
                await ctx.send('You\'re already registered, dming you your token')
                await user.send(f'Here\'s your token again, don\'t lose it this time! ```{token_}```\n'
                                'Did you want to regenerate your token? Run `unregister` and then '
                                'run `register` again to switch to bot-hosting and `refresh` to regenerate a token.')
                # TODO user react to delete message
            else:
                if active_:  # account is active
                    await ctx.send('You\'re already registered!')
                else:  # account deactivated
                    await ctx.send('You seem to have deactivated your account, I will need to acquire your credentials '
                                   'again. (If you changed your prefix it has been reset to `b!`)')
                    await firestore.update_field(uid, 'prefix', 'b!')
                await _complete_user_info()

        else:
            await user.send('Hello! Please reply with either the required information or with `self` to self-host. '
                            'After 45 seconds I get bored and you will have to run the command again.')
            resp = await self._get_user_token(user)
            if not resp:
                return
            if resp == 'self':
                await firestore.add_user(uid, username=user.name, self_=True)
                await user.send(await _self_host(user))
            else:
                token_ = resp
                email = await self._get_user_email(user)
                pwd = await self._get_user_pwd(user)
                await firestore.add_user(uid, username=user.name, self_=False, token=token_, email=email, pwd=pwd)
                await _add_commands_settings(uid)
                await user.send('That\'s it! The bot can now change your status and avatar. The default prefix is '
                                '`b!`\n '
                                'If at anytime you need to change the information you entered or switch to '
                                'self-hosting, '
                                'just run register again')


def setup(bot):
    info.Info(
        name='register',
        brief='register with bot',
        description='register with the bot to use its functions, either self-host or provide token/email/pwd',
        usage='`b!register`'
    ).export(vars_.info_)

    bot.add_cog(Register(bot))
