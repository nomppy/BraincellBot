import os
import re
import time

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

load_dotenv()

from mods import firestore, vars_
from mods import admin

BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(''))

mods = vars_.mods
ignore = vars_.ignore
BOT_TOKEN = os.getenv('BOT_TOKEN')


@commands.command()
@commands.is_owner()
async def reload(ctx, modext=None):
    st = discord.Embed(
        title='Reload',
    ).set_thumbnail(url=bot.user.avatar_url)
    if modext in ['-a', 'all', '--all']:
        st.description = await admin.reload_all(bot, mods, ignore)
        st.colour = vars_.colour_success
    elif not modext:
        st.description = "Here's a list of reloadable modules/extensions"
        st.add_field(name='field1', value='value1')
        st.add_field(name='field2', value='value2')
        st.add_field(name='field1', value='value1')
        st.add_field(name='field1', value='value1')
        st.add_field(name='field1', value='value1')
        st.set_footer(text='footer text', icon_url=bot.user.avatar_url)
        st.colour = bot.user.colour
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
    await admin.reload_all(bot, mods, ignore)


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
        await bot.get_command('counter')(await bot.get_context(message), mentioned)
        return

    if re.match(rf"^<@!?{bot.user.id}>$", message.content):
        if user_:
            await message.channel.send(f'Hewwo {message.author.mention} your prefix is '
                                       f"**{user_['prefix']}**")
            return
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return

    if message.content == 'b!register':
        await bot.get_command('register')(await bot.get_context(message))
        return
    if not user_ and message.content.startswith('b!'):
        await message.channel.send("You're not registered. \U0001F641 Run `b!register` to register.")
        return
    if user_:  # if user not in database or account inactive
        if not user_['active'] and message.guild is not None:
            await message.channel.send("Your account is deactivated. Activate it by running `b!register`.")
            return
        else:
            prefix = user_['prefix']
            if message.content.startswith(prefix):
                message.content = message.content[len(prefix):]
                try:
                    await bot.process_commands(message)
                except CommandNotFound:
                    await message.channel.send("That command doesn't exist.")
                    return


bot.run(BOT_TOKEN)
