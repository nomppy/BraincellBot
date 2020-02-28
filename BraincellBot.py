import discord
import time

from discord.ext.commands import CommandOnCooldown, CommandError
from dotenv import load_dotenv
from ChangeStatus import change_status
from keep_alive import keep_alive
from discord.ext import commands
from io import BytesIO
from discord.ext.commands.cooldowns import BucketType
from PIL import Image
import aiohttp

load_dotenv()
BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix=BOT_PREFIX)

# TOKEN = os.getenv('BOT_TOKEN')
TOKEN = 'NjgyMjQzMzA0Mjg4NjgyMDc2.XlaKrg.QWSxX0dH4ubvlav19LYvU206vuo'
GUILD_ID = 585948652644859904
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281


# class CommandOnCooldown(CommandError):
#     def __init__(self, cooldown, retry_after):
#         self.cooldown = cooldown
#         self.retry_after = retry_after
#         super().__init__('You are on cooldown. Try again in {:.2f}s'.format(retry_after))
#         await


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


@commands.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency, 1)}ms')


@commands.cooldown(1, 10, commands.BucketType.member)
@commands.command(aliases=['cat', 'sendcat', 'catpls', 'bestanimal', 'plscat'])
async def meow(ctx):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            image_link = ''
            while not image_link.endswith('jpg') or image_link.endswith('png'):
                response = await session.get('https://api.thecatapi.com/v1/images/search')
                resp_json = await response.json()
                image_link = resp_json[0]['url']
                print(image_link)
                if image_link.endswith('jpg') or image_link.endswith('png'):
                    # resp = await session.get(image_link)
                    # buffer = BytesIO(await resp.read())
                    # await ctx.send(file=discord.File(buffer, filename='cat.jpg'))  # uploaded image
                    await ctx.send(embed=discord.Embed().set_image(url=image_link))  # embeded image


@meow.error
async def meow_error(ctx, error):
    await ctx.send(error)


bot.add_command(ping)
bot.add_command(meow)


async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


last_change = time.mktime(time.gmtime(0))


@bot.event
async def on_message(message):
    global last_change
    server = bot.get_guild(GUILD_ID)
    if message.content in ['meow'] + bot.get_command('meow').aliases:
        ctx = await bot.get_context(message)
        print(bot.get_command('meow').is_on_cooldown(await bot.get_context(message)))
        if bot.get_command('meow').is_on_cooldown(await bot.get_context(message)):
            await ctx.send('On cooldown.')
        else:
            await meow(ctx)

    # spes = server.get_member(USER_ID)
    # if message.channel == server.get_channel(681628374158147692):
    #     if server.get_role(681628171778785281) in message.author.roles:  # if author has the role
    #         if 'braincells--' in message.content.lower() or 'braincells++' in message.content.lower():
    #             if (time.time() - last_change) < 600 and message.author != spes:
    #                 await message.channel.send(f'Give his braincells a break! Wait {600-int(time.time()-last_change)} seconds')
    #             elif len(message.mentions) != 1 or message.mentions[0].id != USER_ID:
    #                 await message.channel.send('Invalid mentions!')
    #             else:
    #                 with open('braincell_count', 'r') as f:
    #                     count = int(f.read())
    #                 print(f'Current Braincell Count: {count}')
    #                 async with message.channel.typing():
    #                     if 'braincells++' in message.content.lower():
    #                         count = count + 1
    #                     elif 'braincells--' in message.content.lower():
    #                         count = count - 1
    #                     change_status(f"Braincell Counter: {count}")
    #                     last_change = time.time()
    #                 with open('braincell_count', 'w') as f:
    #                     f.write(str(count))
    #                 await message.channel.send('Braincell Counter successfully updated.')
    await bot.process_commands(message)


keep_alive()
bot.run(TOKEN)
