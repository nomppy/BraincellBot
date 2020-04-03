import discord
from discord.ext import commands
from mods import info, vars_


@commands.command(name='help')
async def send_help(ctx, command=None):
    embed = discord.Embed(
        title='Help',
        colour=ctx.guild.me.colour,
    ).set_footer(text=vars_.default_footer_text)
    if not command:
        [
            embed.add_field(
                name=cat,
                value=', '.join([
                    f'`{str(set_)}`'
                    for set_ in vars_.info_[cat].keys()
                ]),
                inline=False)
            for cat in vars_.info_.keys()
        ]
        embed.description = 'Use `help command` to get more help on a specific command'
    elif command not in info.get_all_commands().keys():
        embed.description = 'No help available for this command'
        embed.colour = vars_.colour_error
    else:
        c = info.get_all_commands()[command]
        embed.title = f'Help - {command}'
        [
            embed.add_field(
                name=n,
                value=v,
                inline=False,
            )
            for n, v in c.get_help().items()
            if v is not None
        ]
    await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='help',
        brief='Shows this help text',
        usage='`help [command]`',
        category='Info',
    )
    bot.remove_command('help')
    bot.add_command(send_help)
