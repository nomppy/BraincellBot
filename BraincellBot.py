import os
import time

from discord.ext import commands
from dotenv import load_dotenv
import importlib

from mods import admin
from mods.core import change_status
from keep_alive import keep_alive

load_dotenv()
BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix='b!')

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
        await ctx.send(admin.reload_all(bot, mods))
    elif modext in mods:
        mods[modext] = importlib.reload(mods[modext])
        await ctx.send(f'Reloaded module: {modext}')
    elif f'exts.{modext}' in bot.extensions:
        bot.reload_extension(f'exts.{modext}')
        await ctx.send(f'Reloaded extension: {modext}')
    elif not modext:
        await ctx.send(mods)
        await ctx.send(bot.extensions)


@commands.command()
@commands.is_owner()
async def load(ctx, modext=None):
    try:
        mods[modext] = importlib.import_module(f'mods.{modext}')
        await ctx.send(f'Loaded module: {modext}')
    except ModuleNotFoundError:
        try:
            bot.load_extension(f'exts.{modext}')
            await ctx.send(f'Loaded extension: {modext}')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'Extension **{modext}** already loaded')
        except commands.ExtensionNotFound:
            await ctx.send(f'Module/extension does not exist')


bot.add_command(reload)
bot.add_command(load)
mods = {}
ignore = ['uptimecheck.py']  # ignore on loading phase; for debugging purposes


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # load all commands/cogs
    for file in os.listdir('./exts/'):
        if file.endswith('.py') and file not in ignore:
            ext = file.split('.')[0]
            bot.load_extension(f'exts.{ext}')
            print(f"Loaded command: {ext}")
    # load all non-command functions
    for file in os.listdir('./mods/'):
        if file.endswith('.py') and file not in ignore:
            mod = file.split('.')[0]
            mods[mod] = importlib.import_module(f'mods.{mod}')
            print(f"Loaded module: {mod}")


last_braincell = time.mktime(time.gmtime(0))
last_meow = time.mktime(time.gmtime(0))
just_tried = False


@bot.event
async def on_message(message):
    global last_braincell
    global last_meow
    global just_tried
    server = bot.get_guild(GUILD_ID)
    spes = server.get_member(USER_ID)
    if message.channel == server.get_channel(681628374158147692):
        if server.get_role(681628171778785281) in message.author.roles:  # if author has the role
            if 'braincells--' in message.content.lower() or 'braincells++' in message.content.lower():
                if (time.time() - last_braincell) < 600 and message.author != spes:
                    await message.channel.send('Give his braincells a break! Wait '
                                               f'{600 - int(time.time() - last_braincell)} '
                                               'seconds')
                elif len(message.mentions) != 1 or message.mentions[0].id != USER_ID:
                    await message.channel.send('Invalid mentions!')
                else:
                    with open('braincell_count', 'r') as f:
                        count = int(f.read())
                    print(f'Current Braincell Count: {count}')
                    async with message.channel.typing():
                        if 'braincells++' in message.content.lower():
                            count = count + 1
                        elif 'braincells--' in message.content.lower():
                            count = count - 1
                        await change_status(f"Braincell Counter: {count}")
                        last_braincell = time.time()
                    with open('braincell_count', 'w') as f:
                        f.write(str(count))
                    await message.channel.send('Braincell Counter successfully updated.')
    await bot.process_commands(message)


keep_alive()
bot.run(BOT_TOKEN)
