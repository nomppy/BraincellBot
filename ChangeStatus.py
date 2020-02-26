def change_status(message):
    import requests
    import os
    import json
    from dotenv import load_dotenv

    load_dotenv()

    token = os.getenv('USER_TOKEN')
    print(message)
    headers = {
        'authority': 'discordapp.com',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzgyLjAuNDA2OS4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiI4Mi4wLjQwNjkuMCIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo1NTA0MSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        'authorization': token,
        'accept-language': 'en-US',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4069.0 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://discordapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://discordapp.com/channels/@me',
        'cookie': '__cfduid=d198f079f20644b40f6af9f0e74a1212b1582682742; locale=en-US; __cfruid=31d0a638dfd4c53d085bd13bac0fa9b82057044a-1582682742',
    }
    # status = '{"custom_status":{"text":' + message + '}}}'
    status = {
        "custom_status": {
            "text": message
        }
    }
    status_str = json.dumps(status, separators=(',', ':'))
    # status_str = '{"custom_status":{"text":"' + message + '"}}'
    print(status_str)
    response = requests.patch('https://discordapp.com/api/v6/users/@me/settings', headers=headers, data=status_str)
