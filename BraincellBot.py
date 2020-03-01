import asyncio
import discord
import time
import os
import aiohttp
import random

from dotenv import load_dotenv
from ChangeStatus import change_status
from ChangePfp import change_pfp
from keep_alive import keep_alive
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


load_dotenv()
BOT_PREFIX = 'b!'
bot = commands.Bot(command_prefix='b!')

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = 585948652644859904
USER_ID = 179701226995318785
ROLE_ID = 681628171778785281

stop_timer = False


@commands.command()
@commands.is_owner()
async def pfptimer(ctx, op='display', timer=0, lenience=300):
    global stop_timer
    stop_timer = True
    if op in ['display', 'show', 'list']:
        await ctx.send(f'newpfp timer: {timer} (0 is off)')
    elif op == 'set':
        if timer == 0:
            await ctx.send('`b!newpfp` timer has been turned off.')
            stop_timer = True
        else:
            stop_timer = False
            await ctx.send(f'`b!newpfp` is now set to trigger every {timer} (+- {lenience})seconds')
            while timer != 0 and not stop_timer:
                await asyncio.sleep(timer - lenience + random.randint(0, lenience*2))
                await newpfp(ctx)


@commands.command()
@commands.cooldown(1, 3, BucketType.member)
async def alive(ctx):
    resp = ['Living the dream!', 'Alive and kicking!', 'Yes, but dead inside :(', 'We\'re all gonna die anyway']
    await ctx.send(resp[random.randint(0, len(resp)-1)])


@alive.error
async def alive_error(ctx, err):
    await ctx.send('This command is on cooldown, but I guess I must be alive!')


@commands.command()
@commands.cooldown(1, 60, BucketType.member)
@commands.is_owner()
async def newpfp(ctx, arg='random'):
    async with ctx.typing():
        img_link = await get_cat_link()
        if arg[-3:] in ['jpg', 'png']:
            img_link = arg
        elif len(ctx.message.attachments) == 1:
            img_link = ctx.message.attachments[0].url
        # print(img_link)
        status = await change_pfp(img_link)
    await ctx.send(status)


@newpfp.error
async def newpfp_error(ctx, err):
    print(err)
    await ctx.send(err)


async def get_cat_link():
    async with aiohttp.ClientSession() as session:
        image_link = ''
        while not image_link[-3:] in ['jpg', 'png']:
            response = await session.get('https://api.thecatapi.com/v1/images/search')
            resp_json = await response.json()
            image_link = resp_json[0]['url']
            if image_link[-3:] in ['jpg', 'png']:
                return image_link


async def meow(ctx):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            image_link = await get_cat_link()
            await ctx.send(embed=discord.Embed().set_image(url=image_link))  # embeded image
            # resp = await session.get(image_link)
            # buffer = BytesIO(await resp.read())
            # await ctx.send(file=discord.File(buffer, filename='cat.jpg'))  # uploaded image


bot.add_command(newpfp)
bot.add_command(alive)
bot.add_command(pfptimer)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


last_braincell = time.mktime(time.gmtime(0))
last_meow = time.mktime(time.gmtime(0))
just_tried = False


@bot.event
async def on_message(message):
    global last_braincell
    global last_meow
    global just_tried
    server = bot.get_guild(GUILD_ID)
    if message.content in ['meow', 'catpls', 'plscat', 'bestanimal', 'cat']:
        ctx = await bot.get_context(message)
        if time.time() - last_meow < 5:
            if just_tried:
                await ctx.send('Didn\'t you just try to do this?')
            else:
                await ctx.send('We don\'t want to get banned from the cat api, so please wait another '
                               f'**{5 - int(time.time() - last_meow)}** seconds')
                just_tried = True
        else:
            await meow(ctx)
            last_meow = time.time()
            just_tried = False

    spes = server.get_member(USER_ID)
    if message.channel == server.get_channel(681628374158147692):
        if server.get_role(681628171778785281) in message.author.roles:  # if author has the role
            if 'braincells--' in message.content.lower() or 'braincells++' in message.content.lower():
                if (time.time() - last_braincell) < 600 and message.author != spes:
                    await message.channel.send('Give his braincells a break! Wait '
                                               f'{600-int(time.time()-last_braincell)} '
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
