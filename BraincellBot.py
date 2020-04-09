import os
import re
import time

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

load_dotenv()

from mods import firestore, vars_, admin, timer
from exts import register

BOT_PREFIX = 'b!'
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(''),
    owner_id=179701226995318785,
)

mods = vars_.mods
ignore = vars_.ignore
first_ready = True
BOT_TOKEN = os.getenv('BOT_TOKEN')


@commands.command()
@commands.is_owner()
async def reload(ctx, modext=None):
    st = discord.Embed(
        title='Reload',
    ).set_thumbnail(url=bot.user.avatar_url).set_footer(text=vars_.default_footer_text)
    if modext in ['-a', 'all', '--all']:
        st.description = await admin.reload_all(bot, mods, ignore)
        st.colour = vars_.colour_success
    elif modext in ['-c', 'complete', '--complete']:
        # Reloads twice to ensure all dependencies are reloaded
        st.description = await admin.reload_all(bot, mods, ignore)
        await admin.reload_all(bot, mods, ignore)
        st.colour = vars_.colour_success
    elif not modext:
        st.description = "Here's a list of reloadable modules/extensions"
        _ = ', '.join([str(mod) for mod in vars_.mods if str(mod) != '_'])
        [
            st.add_field(
                name=cat,
                value=', '.join([
                    f'`{str(set_)}`'
                    for set_ in vars_.info_[cat].keys()
                ]),
                inline=False)
            for cat in vars_.info_.keys()
        ]
        st.add_field(
            name='Modules',
            value=', '.join(
                [
                    f'`{str(mod)}`'
                    for mod in list(vars_.mods.keys())[1:]
                ]
            ),
            inline=False)
        st.colour = ctx.guild.me.colour
    else:
        try:
            mods[modext], st.description = await admin.reload_load(modext, mods=mods)
            st.colour = vars_.colour_success
        except ModuleNotFoundError:
            try:
                st.description = await admin.reload_load(modext, bot=bot)
                st.colour = vars_.colour_success
            except commands.ExtensionNotFound:
                st.description = f'Cannot find {modext}'
                st.colour = vars_.colour_error

    await ctx.send(embed=st)


bot.add_command(reload)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    global first_ready
    if first_ready:
        print('First ready')
        await admin.reload_all(bot, mods, ignore)
        await bot.get_user(bot.owner_id).send("I'm online!")
        await vars_.newpfp_timer.run_timer()
        first_ready = False
    await bot.change_presence(activity=discord.Game(name='b!register'))


last_braincell = time.mktime(time.gmtime(0))
last_meow = time.mktime(time.gmtime(0))
just_tried = False


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    user = message.author
    uid = str(user.id)
    user_ = await firestore.get_user(uid)

    # TODO change regex to match the template in database
    if re.match(r"^<@!?[0-9]+> braincells[+\-]{2}", message.content):
        mentioned = message.mentions[0]
        await bot.get_command('counter')(await bot.get_context(message), mentioned.mention)
        return

    if re.match(rf"^<@!?{bot.user.id}>$", message.content):
        if user_:
            await message.channel.send(f'Hello {message.author.mention} your prefix is '
                                       f"**{user_['prefix']}**")
            return
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return
    if not user_ and message.content.startswith('b!'):
        await register.self_host_no_reg(message.author)
        message.content = message.content[2:]
        await bot.process_commands(message)
        return
    if user_:  # if user not in database or account inactive
        if not user_['active'] and message.guild is not None and message.content[2:] not in vars_.unreg:
            await message.channel.send("Your account is deactivated. Activate it by running `b!register`.")
            return
        else:
            prefix = user_['prefix']
            if message.content.startswith(prefix):
                message.content = message.content[len(prefix):]
                if user_['token'] == '!':
                    await message.channel.send(f"{user.mention}*This is a one-time message: "
                                               f"you were automatically registered "
                                               "when you ran a command, to complete registration and gain access to "
                                               f"core features run* `{prefix}register`")
                    await firestore.update_user_field(uid, 'token', None)
                try:
                    await bot.process_commands(message)
                except CommandNotFound:
                    await message.channel.send("That command doesn't exist.")


bot.run(BOT_TOKEN)








