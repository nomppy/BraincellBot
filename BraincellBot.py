import os
import re
import time

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

from mods import firestore
from mods import admin
from mods.core import change_status
from keep_alive import keep_alive
from exts import register

BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(''))

BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
GUILD_ID = 671052553705750580
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281


# TODO write server code to receive register requests
# TODO server code to write to database
# TODO replace messages with embeds


@commands.command()
@commands.is_owner()
async def reload(ctx, modext=None):
    if modext in ['-a', 'all', '--all']:
        st = await admin.reload_all(bot, mods, ignore)
    elif not modext:
        st = 'TODO: send list of modules/extensions here'
    else:
        try:
            mods[modext], st = await admin.reload_load(modext, mods=mods)
        except ModuleNotFoundError:
            try:
                st = await admin.reload_load(modext, bot=bot)
            except commands.ExtensionNotFound:
                st = f'Cannot find {modext}'

    await ctx.send(st)


bot.add_command(reload)
mods = {'_': '_'}
ignore = ['_', 'uptimecheck.py']  # ignore on loading phase; for debugging purposes


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
    if re.match(r"^<@!?[0-9]+> braincells[+\-]{2}$", message.content):
        await bot.get_command('counter')(await bot.get_context(message), user)
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
                await bot.process_commands(message)


keep_alive()
bot.run(BOT_TOKEN)
