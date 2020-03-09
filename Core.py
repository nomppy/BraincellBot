import json
import aiohttp
from dotenv import load_dotenv
import os
import base64


load_dotenv()
token = os.getenv('USER_TOKEN')
headers = {
    'authority': 'discordapp.com',
    'authorization': token,
    'accept-language': 'en-US',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/82.0.4069.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://discordapp.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://discordapp.com/channels/@me'
}


async def change_avatar(img_link):
    file_ext = img_link.split('.')[-1]
    if file_ext != 'png' and file_ext != 'jpg':
        return 'Image type not supported.'

    async with aiohttp.ClientSession() as session:
        resp = await session.get(img_link)
        img_b64 = base64.b64encode(await resp.read()).decode()
        data = {
            'username': os.getenv('USER_NAME'),
            'email': os.getenv('USER_EMAIL'),
            'password': os.getenv('USER_PASSWORD'),
            'avatar': f'data:{resp.content_type};base64,{img_b64}',
            'discriminator': None,
            'new_password': None
        }
        data = json.dumps(data, separators=(',', ':'))
        response = await session.patch('https://discordapp.com/api/v6/users/@me',
                                       headers=headers,
                                       data=data)
        if response.status == 200:
            return 'Avatar successfully updated.'
        else:
            return 'Something funky wonky happened :('


async def change_status(message):
    status = {
        'custom_status': {
            'text': message
        }
    }
    status = json.dumps(status, separators=(',', ':'))
    async with aiohttp.ClientSession() as session:
        response = await session.patch('https://discordapp.com/api/v6/users/@me/settings',
                                       headers=headers,
                                       data=status)


async def get_cat_link():
    async with aiohttp.ClientSession() as session:
        image_link = ''
        while not image_link[-3:] in ['jpg', 'png']:
            response = await session.get('https://api.thecatapi.com/v1/images/search')
            resp_json = await response.json()
            image_link = resp_json[0]['url']
            if image_link[-3:] in ['jpg', 'png']:
                return image_link
