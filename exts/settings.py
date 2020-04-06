import discord
from discord.ext import commands
from mods import firestore, info, vars_


async def _embed_available_settings(command, embed):
    for setting in command.get_settings():
        options = ""
        opt = command.get_options(setting)
        if type(opt) is list:
            [options.join(opt) for opt in command.get_options(setting)]
        else:
            if opt == 'any':
                options += "any string"
            elif opt == 'int':
                options += 'any number'
            elif opt == 'none':
                options += 'toggle true/false'
            else:
                options += opt

        embed.add_field(name=f'{setting} ({command.default[setting]})', value=options, inline=False)
    return embed


@commands.command()
async def settings(ctx, command=None, field=None, value=None):
    uid = str(ctx.author.id)
    command_ = await firestore.get_command(uid, command)
    embed = discord.Embed(
        title="Settings",
        colour=ctx.guild.me.colour
    ).set_footer(text=vars_.default_footer_text)
    _commands = info.get_all_commands()

    if not command:
        configurable = []
        [configurable.append(key) for key, command in _commands.items() if command.configurable()]
        embed.description = f"Use `settings <option>` to view available settings"
        [embed.add_field(name=config, value=f'`settings {config}`') for config in configurable]
        embed.colour = ctx.guild.me.colour
    elif command not in _commands.keys():
        embed.description = "Command does not exist"
        embed.colour = vars_.colour_error
    elif command and not field or command and field not in _commands[command].get_settings():
        embed.title = f'Settings - {command}'
        embed.description = f"These are the available settings for {command} (defaults in parenthesis)"
        embed = await _embed_available_settings(_commands[command], embed)
    elif not command or not field or not value:
        embed.description = "Incorrect syntax, see `help settings`"
        embed.colour = vars_.colour_error
    elif not _commands[command].validate_setting(field, value):
        embed.title = f'Settings - {command}'
        embed.description = "That isn't a valid option for this setting"
        embed.colour = vars_.colour_error
    else:
        if _commands[command].get_options(field) is None:
            value = not command_[field]
        await firestore.update_command_field(uid, command, field, value)
        embed.title = f'Settings - {command}'
        embed.description = f"{field} has been set to {value}"
        embed.colour = vars_.colour_success
    await ctx.send(embed=embed)


def setup(bot):
    info.Info(
        name='settings',
        brief='configure things for commands',
        usage='settings [command] [option] [value]',
        category='Account'
    ).export(vars_.info_)

    bot.add_command(settings)
