from google.cloud import monitoring_v3
from discord.ext import commands
import pprint


class UptimeCheckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, host_name, path, display_name, project_id='projects/braincell-bot-dpy'):
        config = monitoring_v3.types.uptime_pb2.UptimeCheckConfig()
        config.display_name = display_name
        config.monitored_resource.type = 'uptime_url'
        config.monitored_resource.labels.update({'host': host_name})
        config.http_check.path = path
        config.http_check.port = 80
        config.timeout.seconds = 10
        config.period.seconds = 300

        client = monitoring_v3.UptimeCheckServiceClient()
        new_config = client.create_uptime_check_config(project_id, config)
        pprint.pprint(new_config)
        return new_config

    @commands.command()
    async def get(self, ctx, config_name):
        client = monitoring_v3.UptimeCheckServiceClient()
        config = client.get_uptime_check_config(config_name)
        return config

    @commands.command()
    async def update(self, ctx, config_name, new_display_name=None, new_http_check_path=None):
        client = monitoring_v3.UptimeCheckServiceClient()
        config = client.get_uptime_check_config(config_name)
        # field_mask = monitoring_v3.types.


def setup(bot):
    bot.add_cog(UptimeCheckCog(bot))
