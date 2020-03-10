from google.cloud import monitoring_v3
from discord.ext import commands
import pprint


def setup(bot):
    class UptimeCheck(commands.Cog, name='uptimecheck'):
        def __init__(self, bot_):
            self.bot = bot_
            self.client = monitoring_v3.UptimeCheckServiceClient()
            self.parent = 'projects/braincell-bot-dpy'

        @commands.command()
        async def uptime_check(self, ctx, action='create', url=''):
            client = monitoring_v3.UptimeCheckServiceClient()

            # TODO pass parameters
            if action == 'create':
                config = {
                    'display_name': ctx.author.id,

                }
                result = self.client.create_uptime_check_config(
                    parent='projects/braincell-bot-dpy',
                    uptime_check_config=config,
                    timeout=10
                )
            elif action == 'get':
                result = client.get_uptime_check_config()
            elif action == 'update':
                result = client.update_uptime_check_config()
            elif action == 'delete':
                result = client.delete_uptime_check_config()