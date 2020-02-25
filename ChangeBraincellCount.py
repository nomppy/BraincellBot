import discord
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
TOKEN = os.getenv('USER_TOKEN')
# GUILD_ID = 585948652644859904
# USER_ID = 179701226995318785
# CHANNEL_ID = 622450759065403402

count = sys.argv[1]
print(f'Target Braincell Count: {count}')


@client.event
async def on_connect():
    await client.change_presence(activity=discord.Activity(type=3, name=f'my Braincell Count drop: {count}'))


client.run(TOKEN, bot=False)
# async with typing() ;) infinitetypppp
