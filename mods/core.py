import json
import aiohttp
import base64


headers = {
    'authority': 'discord.com',
    'accept-language': 'en-US',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/82.0.4069.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://discord.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://discord.com/channels/@me'
}


async def change_avatar(user_: dict, img_link):
    file_ext = img_link.split('.')[-1]
    if file_ext != 'png' and file_ext != 'jpg':
        return 'Image type not supported.', False

    async with aiohttp.ClientSession() as session:
        resp = await session.get(img_link)
        img_b64 = base64.b64encode(await resp.read()).decode()

        data = {
            'username': user_['username'],
            'email': user_['email'],
            'password': user_['pwd'],
            'avatar': f'data:{resp.content_type};base64,{img_b64}',
            'discriminator': None,
            'new_password': None
        }
        headers['authorization'] = user_['token']
        data = json.dumps(data, separators=(',', ':'))
        response = await session.patch('https://discord.com/api/v6/users/@me',
                                       headers=headers,
                                       data=data)
        await session.close()
        if response.status == 200:
            return 'Avatar successfully updated.', True
        else:
            return 'Something funky wonky happened :(', False


async def change_status(token_, message):
    status = {
        'custom_status': {
            'text': message
        }
    }
    headers['authorization'] = token_
    status = json.dumps(status, separators=(',', ':'))
    async with aiohttp.ClientSession() as session:
        response = await session.patch('https://discord.com/api/v6/users/@me/settings',
                                       headers=headers,
                                       data=status)
        await session.close()
        return response


async def get_cat_link():
    async with aiohttp.ClientSession() as session:
        image_link = ''
        while not image_link[-3:] in ['jpg', 'png']:
            response = await session.get('https://api.thecatapi.com/v1/images/search')
            resp_json = await response.json()
            image_link = resp_json[0]['url']
            await session.close()
            if image_link[-3:] in ['jpg', 'png']:
                return image_link
            return
