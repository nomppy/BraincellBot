from google.cloud import monitoring_v3
from discord.ext import commands
from urllib.parse import urlparse


class UptimeCheck(commands.Cog, name='uptimecheck'):
    def __init__(self, bot_):
        self.bot = bot_
        self.client = monitoring_v3.UptimeCheckServiceClient()
        self.project_name = 'projects/braincell-bot-dpy'

    @commands.command(name='uptimecheck', aliases=['utc'])
    async def uptime_check(self, ctx, url='', action='create'):
        path = urlparse(url).path
        host = urlparse(url).hostname

        if action == 'create':
            name, status = await self._create_uptime_check_config(host, path, ctx.author.id)
            await ctx.send(name)
            await ctx.send(status)
        elif action == 'get':
            name = f'{self.project_name}/uptimeCheckConfigs/{ctx.author.id}'
            await ctx.send(
                await self._get_uptime_check_config(name)
            )

    @uptime_check.error
    async def uptime_check_err(self, ctx, err):
        await ctx.send(err)

    async def _create_uptime_check_config(self, host_name, path, display_name):
        config = monitoring_v3.types.uptime_pb2.UptimeCheckConfig()
        config.display_name = str(display_name)
        config.monitored_resource.type = 'uptime_url'
        config.monitored_resource.labels.update(
            {'host': host_name}
        )
        config.http_check.path = path
        config.timeout.seconds = 10
        config.period.seconds = 300

        _ = self.client.create_uptime_check_config(self.project_name, config)
        if _.name:
            return _.name, 'Uptime check created successfully!'
        return 'Something went wrong :('

    async def _get_uptime_check_config(self, config_name):
        return self.client.get_uptime_check_config(config_name)

    async def _update_uptime_check_config(self, config_name, new_name=None, new_path=None):
        config = self.client.get_uptime_check_config(config_name)
        if new_name:
            config.display_name = new_name
        if new_path:
            config.http_check.path = new_path

        return self.client.update_uptime_check_config(config)

    async def _delete_uptime_check_config(self, config_name):
        self.client.delete_uptime_check_config(config_name)
        return f'Deleted uptime check: {config_name}'


def setup(bot):
    bot.add_cog(UptimeCheck(bot))
