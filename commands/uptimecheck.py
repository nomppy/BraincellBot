from google.cloud import monitoring_v3
from discord.ext import commands
import pprint


@commands.command(name='uptimecheck')
async def uptime_check(ctx, action='create'):
    client = monitoring_v3.UptimeCheckServiceClient()

    # TODO pass parameters
    if action == 'create':
        result = client.create_uptime_check_config()
    elif action == 'get':
        result = client.get_uptime_check_config()
    elif action == 'update':
        result = client.update_uptime_check_config()
    elif action == 'delete':
        result = client.delete_uptime_check_config()